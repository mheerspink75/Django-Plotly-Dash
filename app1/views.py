from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect

from app1.dashapps import stock_charts2
from app1.dashapps import crypto_quotes

import requests
import json



# Get BTC Price Data
bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
bitcoin_price = json.loads(bitcoin_price_request.content)


##### Main Pages #####

def home(request):
    return render(request, 'app1/pages/index.html')


def DASHBOARD(request):
    test = request.user.account.user # User.objects.get(id=1).account.user

    # Get User Info
    usd_balance = request.user.account.usd_balance
    bitcoin_balance = request.user.account.bitcoin_balance
    user_btc_balance = (float(bitcoin_balance) * bitcoin_price['USD'])

    # Calculate Portfolio Balance
    math = ((user_btc_balance) + float(usd_balance))
    portfolio_balance = str(math)

    return render(request, 'app1/pages/DASHBOARD.html',
                  {'bitcoin_price': bitcoin_price,
                   'usd_balance': usd_balance,
                   'portfolio_balance': portfolio_balance,
                   'user_btc_balance': user_btc_balance,
                   'test': test})


def stocks(request):
    return render(request, 'app1/pages/stocks.html')


def account(request):
    return render(request, 'app1/pages/account.html',
                  {'bitcoin_price': bitcoin_price})


#### Registration/Login #####

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():

            print(response.POST['username'])
            print(response.POST)
            try:
                User.objects.get(username = response.POST['username'])
            except User.DoesNotExist:
                print('User does not exist')
            form.save()
            return redirect(home)
    else:
        form = RegisterForm()
    return render(response, 'registration/register.html', {"form": form})

