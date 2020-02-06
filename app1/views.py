from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Account
import datetime

from app1.dashapps import crypto_quotes
from app1.dashapps import crypto_charts2

import requests
import json


# Get BTC Price Data
bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
bitcoin_price = json.loads(bitcoin_price_request.content)

# Get News Feed
news_request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
news = json.loads(news_request.content)

# Get BTC Full Data
coins = 'BTC'
symbol_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coins + '&tsyms=USD')
symbol = json.loads(symbol_request.content)

crypto_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD')


##### Main Pages #####

def home(request):
    return render(request, 'app1/pages/index.html')


def DASHBOARD(request):
    # Get user info from db
    usd_balance = request.user.account.usd_balance
    bitcoin_balance = request.user.account.bitcoin_balance

    # Calculate the BTC/USD value
    user_btc_balance = round((float(bitcoin_balance) * bitcoin_price['USD']), 2)
    
    # Calculate the total porfolio balance
    portfolio_balance = ((user_btc_balance) + float(usd_balance))

    return render(request, 'app1/pages/DASHBOARD.html',
                  {'bitcoin_price': bitcoin_price,
                   'usd_balance': usd_balance,
                   'portfolio_balance': portfolio_balance,
                   'user_btc_balance': user_btc_balance})

def markets(request):
    return render(request, 'app1/pages/markets.html',
                    {'symbol': symbol})

def quotes(request):
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        crypto = symbol
    return render(request, 'app1/pages/quotes.html', {'crypto': crypto})
   

def crypto_news(request):
    return render(request, 'app1/pages/crypto_news.html',
                  {'news': news})


def test_page(request):
    # Get BTC Price Data
    bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    bitcoin_price = json.loads(bitcoin_price_request.content)

    # Get BTC Full Data
    coins = 'BTC'
    symbol_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coins + '&tsyms=USD')
    symbol = json.loads(symbol_request.content)

    # Get user info from db
    usd_balance = request.user.account.usd_balance
    bitcoin_balance = request.user.account.bitcoin_balance

    # Calculate the BTC/USD value
    user_btc_balance = round((float(bitcoin_balance) * bitcoin_price['USD']), 2)
    
    # Calculate the total porfolio balance
    portfolio_balance = round((user_btc_balance) + float(usd_balance), 2)

    if request.method == "POST":
        # Print BTC Existing Quantity
        print("---pre save---\nexisting BTC quantity: ", bitcoin_balance)

        # Buy BTC Quantity
        buy_BTC = request.POST['buy_BTC']
        print("buy/sell btc quantity: ", buy_BTC)

        # USD Value of Purchase Amount
        usd_value = (float(buy_BTC) * bitcoin_price['USD'])
        print("buy/sell btc quantity (usd value): ", usd_value)

        # Add BTC Quantity
        add_BTC =round((float(buy_BTC) + float(bitcoin_balance)), 2)
        print("add/subtract btc buy/sell quantity to/from existing btc quantity: ", add_BTC)

        # Pay for the BTC with Cash
        usd_sale = round(float(usd_balance) - (usd_value), 2)
        print("portfolio total USD balance after sale: ", usd_sale)

        # Save to the Database
        x = request.user.account
        x.bitcoin_balance = add_BTC
        x.usd_balance = usd_sale
        x.save()

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
        user_btc_balance = round((float(bitcoin_balance) * bitcoin_price['USD']), 2)
        print("user btc balance: ", user_btc_balance)

        # Calculate the total porfolio balance
        portfolio_balance = round((user_btc_balance) + float(usd_balance), 2)
        print("portfolio balance: ", portfolio_balance)

        return render(request, 'app1/pages/test_page.html',
                  {'bitcoin_price': bitcoin_price,
                   'usd_balance': usd_balance,
                   'portfolio_balance': portfolio_balance,
                   'user_btc_balance': user_btc_balance,
                   'buy_BTC': buy_BTC,
                   'add_BTC': add_BTC,
                   'usd_value': usd_value,
                   'exchange_rate': exchange_rate,
                   'date': date,
                   'symbol': symbol})
    else:
        return render(request, 'app1/pages/test_page.html',
                    {'bitcoin_price': bitcoin_price,
                    'usd_balance': usd_balance,
                    'portfolio_balance': portfolio_balance,
                    'user_btc_balance': user_btc_balance,
                    'symbol': symbol})


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

