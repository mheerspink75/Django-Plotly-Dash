from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Account

import datetime
import requests
import json

from app1.dashapps import crypto_charts2
from app1.dashapps import stock_charts2 


#### Registration/Login #####
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = RegisterForm()
    return render(response, 'registration/register.html', {"form": form})


#### Main Pages ####
def home(request):
    return render(request, 'app1/pages/index.html')


def DASHBOARD(request):
    # Get BTC Price Data
    bitcoin_price_request = requests.get(
        'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    bitcoin_price = json.loads(bitcoin_price_request.content)

    # Get BTC Full Data
    coins = 'BTC'
    symbol_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coins + '&tsyms=USD')
    symbol = json.loads(symbol_request.content)

    # Get user info from db
    usd_balance = request.user.account.usd_balance
    bitcoin_balance = request.user.account.bitcoin_balance

    error = ''

    if request.method == "POST":
        # Print BTC Existing Quantity
        print("existing BTC quantity: ", bitcoin_balance)

        # Select BUY / SELL
        buy_sell = request.POST['buy_sell']
        print(buy_sell)

        # BUY / SELL BTC Quantity
        buy_BTC = float(request.POST['buy_BTC'])
        if buy_sell == 'sell':
            buy_BTC = buy_BTC * -1
        print("buy/sell btc quantity: ", buy_BTC)

        # USD Value of Purchase Amount
        usd_value = (buy_BTC * bitcoin_price['USD'])
        print("buy/sell btc quantity (usd value): ", usd_value)

        # Add BTC Quantity
        add_BTC = round(buy_BTC + float(bitcoin_balance), 2)
        print("add/subtract btc buy/sell quantity to/from existing btc quantity: ", add_BTC)

        # Pay for the BTC with Cash
        usd_sale = round(float(usd_balance) - (usd_value), 2)
        print("portfolio total USD balance after sale: ", usd_sale)

        # Save to the Database
        x = request.user.account
        x.bitcoin_balance = add_BTC
        x.usd_balance = usd_sale

        if x.usd_balance >= 0 and x.bitcoin_balance >= 0:
            print('if', x.usd_balance, x.bitcoin_balance )
            x.save()
            usd_balance = x.usd_balance 
            bitcoin_balance = x.bitcoin_balance
        else:
            error = 'Insufficient funds. Please consult your doctor.'          

    # Calculate the BTC/USD value
    user_btc_balance = round(
        (float(bitcoin_balance) * bitcoin_price['USD']), 2)

    # Calculate the total porfolio balance
    portfolio_balance = round((user_btc_balance) + float(usd_balance), 2)

    return render(request, 'app1/pages/DASHBOARD.html',
                    {'bitcoin_price': bitcoin_price,
                    'usd_balance': usd_balance,
                    'portfolio_balance': portfolio_balance,
                    'user_btc_balance': user_btc_balance,
                    'bitcoin_balance': bitcoin_balance,
                    'symbol': symbol,
                    'error': error})


def quotes(request):
    # Get BTC Full Data
    coins = 'BTC'
    symbol_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coins + '&tsyms=USD')
    symbol = json.loads(symbol_request.content)

    # Get Multiple Currency Full Data
    multi_coin = 'BTC,ETH,BCH,ETC,XRP,BSV,EOS,LTC,TRX,OKB,BNB,DASH'
    mc_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + multi_coin + '&tsyms=USD')
    mc_symbol = json.loads(mc_request.content)

    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get(
            'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        crypto = symbol
    return render(request, 'app1/pages/quotes.html', {'crypto': crypto, 'mc_symbol': mc_symbol})


def crypto_news(request):
    # Get News Feed
    news_request = requests.get(
        'https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    news = json.loads(news_request.content)
    return render(request, 'app1/pages/crypto_news.html', {'news': news})





"""
        # Print Datetime
        date = datetime.datetime.now()
        print(datetime.datetime.now())

        exchange_rate = bitcoin_price['USD']
        print(exchange_rate)

        # Get user info from the Database
        usd_balance = request.user.account.usd_balance
        print("---post save---\nusd balance: ", usd_balance)

        bitcoin_balance = request.user.account.bitcoin_balance
        print("bitcoin quantity", bitcoin_balance)

        # Calculate the BTC/USD value
        user_btc_balance = round(
            (float(bitcoin_balance) * bitcoin_price['USD']), 2)
        print("user btc balance: ", user_btc_balance)

        # Calculate the total porfolio balance
        portfolio_balance = round((user_btc_balance) + float(usd_balance), 2)
        print("portfolio balance: ", portfolio_balance)

        return render(request, 'app1/pages/DASHBOARD.html',
                      {'bitcoin_price': bitcoin_price,
                       'usd_balance': usd_balance,
                       'portfolio_balance': portfolio_balance,
                       'user_btc_balance': user_btc_balance,
                       'buy_BTC': buy_BTC,
                       'add_BTC': add_BTC,
                       'usd_value': usd_value,
                       'exchange_rate': exchange_rate,
                       'date': date,
                       'symbol': symbol,
                       'error': error})
"""