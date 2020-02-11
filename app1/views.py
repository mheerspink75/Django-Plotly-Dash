from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from app1.models import Account, Transactions
import requests
import json


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

"""
def DASHBOARD(request)
    if request.method == "POST":
        insert_order(request)
    else: # request.method is "GET".
        nav_data = prepare_navigation_menu_data(request)
        balance_data = prepare_render_balance_data(request)
        order_form_data = prepare_render_order_form_data(request)
        transaction_history_data = prepare_render_transaction_history_data(request)
        return render(request, 'template_url.html', {"menu_items": nav_data.menu_items, "balance_data": balance_data, ...})

        for item in nav_data.menu_items:
"""

@login_required
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
    usd_balance = float(request.user.account.usd_balance)
    bitcoin_balance = float(request.user.account.bitcoin_balance)

    error = ''

    if request.method == "POST":
        # Radio Options Trade BTC / USD
        inlineRadioOptions = request.POST['inlineRadioOptions']
        # Select BUY / SELL
        BUY_SELL = request.POST['BUY_SELL']
        # Input BUY / SELL Amount
        BUY_BTC = float(request.POST['BUY_BTC'])

        # Calculate BTC Trade
        if inlineRadioOptions == 'TRADE_BTC':
            if BUY_SELL == 'SELL':
                BUY_BTC = BUY_BTC * -1
            # USD Value of Sale
            USD_SALE_PRICE = (BUY_BTC * bitcoin_price['USD'])
            # Update BTC Balance
            UPDATE_BTC = round(BUY_BTC + bitcoin_balance, 2)
            # Update USD Balance
            UPDATE_USD = round(usd_balance - USD_SALE_PRICE, 2)

        # Calculate USD Trade
        if inlineRadioOptions == 'TRADE_USD':
            if BUY_SELL == 'BUY':
                BUY_BTC = BUY_BTC * -1
            # Update USD Balance
            UPDATE_USD = round(BUY_BTC + usd_balance, 2)
            # Update BTC Balance
            USD_SALE_PRICE = BUY_BTC * -1
            BUY_BTC = round((USD_SALE_PRICE / bitcoin_price['USD']), 2)
            UPDATE_BTC = BUY_BTC + bitcoin_balance

        # Update the Database
        x = request.user.account
        x.bitcoin_balance = UPDATE_BTC
        x.usd_balance = UPDATE_USD

        # Check for insufficient funds
        if x.usd_balance >= 0 and x.bitcoin_balance >= .001:
            # Create Transaction Table Entry
            Transactions.objects.create(user_id=request.user.id,
                                        transaction_usd_price=bitcoin_price['USD'],
                                        transaction_type=BUY_SELL, transaction_date=timezone.datetime.now(),
                                        transaction_btc_quantity=BUY_BTC,
                                        transaction_total_usd_price=(USD_SALE_PRICE * -1))
            # Save Account Balances to db
            x.save()
            return redirect(DASHBOARD)
        else:
            error = 'Insufficient funds...\n  *** Sale Denied! ***'

    # Calculate the USD value of the user's BTC
    user_btc_balance = round((bitcoin_balance * bitcoin_price['USD']), 2)

    # Calculate the total portfolio balance in USD
    portfolio_balance = round(user_btc_balance + usd_balance, 2)

    # Calculate the percantage of the portfolio invested
    btc_percentage = round((user_btc_balance / portfolio_balance) * 100, 2)
    usd_percentage = round((usd_balance / portfolio_balance) * 100, 2)

    # Display the transaction history of the logged in user
    transaction = Transactions.objects.all().filter(user=request.user).order_by('transaction_date').reverse()

    return render(request, 'app1/pages/DASHBOARD.html',
                  {'bitcoin_price': bitcoin_price,
                   'transaction': transaction,
                   'usd_balance': usd_balance,
                   'portfolio_balance': portfolio_balance,
                   'user_btc_balance': user_btc_balance,
                   'bitcoin_balance': bitcoin_balance,
                   'btc_percentage': btc_percentage,
                   'usd_percentage': usd_percentage,
                   'symbol': symbol,
                   'error': error})


def quotes(request):
    from app1.dashapps import crypto_charts2
    # Get BTC Full Data
    coins = 'BTC'
    symbol_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coins + '&tsyms=USD')
    symbol = json.loads(symbol_request.content)

    # Get Quotes
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get(
            'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        crypto = symbol

    # Get Multiple Currency Full Data
    multi_coin = 'BTC,ETH,BCH,ETC,XRP,BSV,EOS,LTC,TRX,OKB,BNB,DASH'
    mc_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + multi_coin + '&tsyms=USD')
    mc_symbol = json.loads(mc_request.content)

    return render(request, 'app1/pages/quotes.html', {'crypto': crypto, 'mc_symbol': mc_symbol})


def crypto_news(request):
    # Get News Feed
    news_request = requests.get(
        'https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    news = json.loads(news_request.content)
    return render(request, 'app1/pages/crypto_news.html', {'news': news})
