from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from . import models
from app1.models import Account, Transaction

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

    # Get BTC and USD balance from db
    usd_balance = request.user.account.usd_balance
    bitcoin_balance = request.user.account.bitcoin_balance

    # Get transaction history from db
    transaction_history = models.Transaction.objects.order_by('transaction_date')
    print(transaction_history)

    error = ''

    if request.method == "POST":
        # Print BTC Existing Balance before sale
        print("---\nBTC BALANCE: ", bitcoin_balance)
        print("USD BALANCE: $", usd_balance)
        print("PORTFOLIO TOTAL (USD): $", round((float(bitcoin_balance) * bitcoin_price['USD']) + float(usd_balance), 2))

        # Select BUY / SELL
        BUY_SELL = request.POST['BUY_SELL']
        print('---\nBUY/SELL BTC: ', BUY_SELL)

        # BUY / SELL BTC Quantity
        BUY_BTC = float(request.POST['BUY_BTC'])
        if BUY_SELL == 'SELL':
            BUY_BTC = BUY_BTC * -1
            print("SELL BTC Quantity: ", BUY_BTC)
        else:
            print("BUY BTC Quantity: +", BUY_BTC)

        # USD Value of Purchase
        USD_SALE_PRICE = (BUY_BTC * bitcoin_price['USD'])
        if BUY_SELL == 'SELL':
            print("SELL BTC (USD PRICE): + $", (USD_SALE_PRICE * -1))
        else:
            print("BUY BTC (USD PRICE): - $", USD_SALE_PRICE)

        # Update BTC Balance
        UPDATE_BTC = round(BUY_BTC + float(bitcoin_balance), 2)
        print("---\nUPDATE BTC BALANCE : ", UPDATE_BTC)

        # Update USD Balance
        UPDATE_USD = round(float(usd_balance) - (USD_SALE_PRICE), 2)
        print("UPDATE USD BALANCE: $", UPDATE_USD)

        # Save to the Database
        x = request.user.account
        x.bitcoin_balance = UPDATE_BTC
        x.usd_balance = UPDATE_USD

        # Check for insufficient funds update db
        if x.usd_balance >= 0 and x.bitcoin_balance >= 0:
            x.save()
            print('---\nChecking for insufficent funds...\n---', '\n*** Sale Approved! ***\n---',
                  '\nBTC BALANCE (after sale): ',  x.bitcoin_balance, '\nUSD BALANCE (after sale): $',  x.usd_balance)
            print("PORTFOLIO TOTAL (USD): $", round((float(bitcoin_balance) * bitcoin_price['USD']) + float(usd_balance), 2), '\n')
        else:
            error = 'Insufficient funds... ***Sale Denied!***'
            print('---\nChecking for insufficent funds...\n---\n',
                  'Insufficient Funds...\n---\n ***Sale Denied!*** \n')

    # Calculate the BTC (USD) Value
    user_btc_balance = round((float(bitcoin_balance) * bitcoin_price['USD']), 2)

    # Calculate the Portfolio Total (USD) Value
    portfolio_balance = round((user_btc_balance) + float(usd_balance), 2)

    return render(request, 'app1/pages/DASHBOARD.html',
                  {'bitcoin_price': bitcoin_price,
                   'usd_balance': usd_balance,
                   'portfolio_balance': portfolio_balance,
                   'user_btc_balance': user_btc_balance,
                   'bitcoin_balance': bitcoin_balance,
                   'symbol': symbol,
                   'transaction_history': transaction_history,
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

    # Get Quotes
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

