from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect

from app1.dashapps import crypto_quotes

import requests
import json


# Get BTC Price Data
bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
bitcoin_price = json.loads(bitcoin_price_request.content)

# Get News Feed
news_request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
news = json.loads(news_request.content)

# Get BTC Full Data
coins = 'BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX'
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
    user_btc_balance = (float(bitcoin_balance) * bitcoin_price['USD'])
    
    # Calculate the total porfolio balance
    math = ((user_btc_balance) + float(usd_balance))
    portfolio_balance = str(math)

    return render(request, 'app1/pages/DASHBOARD.html',
                  {'bitcoin_price': bitcoin_price,
                   'usd_balance': usd_balance,
                   'portfolio_balance': portfolio_balance,
                   'user_btc_balance': user_btc_balance})

def stocks(request):
    return render(request, 'app1/pages/stocks.html',
                    {'symbol': symbol})

def search(request):
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        crypto = symbol
    return render(request, 'app1/pages/search.html', {'crypto': crypto})
   

def account(request):
    return render(request, 'app1/pages/account.html',
                  {'news': news})


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

