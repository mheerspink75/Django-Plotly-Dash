from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from app1.models import Account, Transactions
import requests
import json
import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from app1.dashapps.crypto_compare import get_btc, symbol, news, mc_symbol


quotes_dash_app = DjangoDash('crypto-quotes')


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


@login_required
def DASHBOARD(request):
    # Get user BTC and USD balance from db
    usd_balance = float(request.user.account.usd_balance)
    bitcoin_balance = float(request.user.account.bitcoin_balance)

    # Get BTC Price
    message = ''
    bitcoin_price = None
    market_data = {
        'DISPLAY': {
            'BTC': {
                'USD': {
                    'FROMSYMBOL': 'BTC',
                    'PRICE': 'Unavailable',
                    'HIGHDAY': 'Unavailable',
                    'LOWDAY': 'Unavailable',
                }
            }
        }
    }

    try:
        bitcoin_price = float(get_btc())
        market_data = symbol(bitcoin_price)
    except (requests.RequestException, RuntimeError, ValueError):
        message = (
            'Live BTC market data is temporarily unavailable. '
            'Trading is disabled until pricing data is restored.'
        )

    if request.method == "POST" and bitcoin_price is not None:
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
            # Set the BTC Quantity Threshold
            BTC_QUANTITY_THRESHOLD = .01
            # USD Value of Sale
            USD_SALE_PRICE = BUY_BTC * bitcoin_price
            # Update BTC Balance Quantity
            UPDATE_BTC = BUY_BTC + bitcoin_balance
            # Update USD Balance
            UPDATE_USD = usd_balance - USD_SALE_PRICE

        # Calculate USD Trade
        if inlineRadioOptions == 'TRADE_USD':
            if BUY_SELL == 'BUY':
                BUY_BTC = BUY_BTC * -1
                BTC_QUANTITY_THRESHOLD = ((BUY_BTC * -1) / bitcoin_price)
            if BUY_SELL == 'SELL':
                BTC_QUANTITY_THRESHOLD =  BUY_BTC / bitcoin_price
            # USD Value of sale
            USD_SALE_PRICE = BUY_BTC * -1
            # Update USD Balance
            UPDATE_USD = BUY_BTC + usd_balance
            # Calculate the BTC Quantity
            BUY_BTC = USD_SALE_PRICE / bitcoin_price
            # Set the BTC Quantity USD Threshold to .001
            BTC_QUANTITY_THRESHOLD = BTC_QUANTITY_THRESHOLD
            # Update BTC Balance Quantity
            UPDATE_BTC = BUY_BTC + bitcoin_balance

        # Update the Database
        x = request.user.account
        x.bitcoin_balance = UPDATE_BTC
        x.usd_balance = UPDATE_USD

        # Check for insufficient funds
        if (x.usd_balance >= 0 and x.bitcoin_balance >= 0) and BTC_QUANTITY_THRESHOLD >= 0.01 :
            # Create Transaction Table Entry
            Transactions.objects.create(user_id=request.user.id,
                                        transaction_usd_price=bitcoin_price,
                                        transaction_type=BUY_SELL,
                                        transaction_date=timezone.datetime.now(),
                                        transaction_btc_quantity=BUY_BTC,
                                        transaction_total_usd_price=(USD_SALE_PRICE * -1))
            x.save()
            return redirect(DASHBOARD)
        else: 
            message = 'Insufficient funds...  *** Sale Denied! ***'
            if BTC_QUANTITY_THRESHOLD < 0.01:
                message = 'BTC Value: < 0.01  *** Sale Denied! ***'
    elif request.method == "POST":
        message = (
            'This trade could not be submitted because live BTC pricing '
            'is temporarily unavailable.'
        )

    # Prepare
    def update():
        # Calculate the USD value of the user's BTC
        effective_price = bitcoin_price or 0
        user_btc_balance = round((bitcoin_balance * effective_price), 2)
        # Calculate the total portfolio balance in USD
        portfolio_balance = user_btc_balance + usd_balance
        # Calculate the percantage of the portfolio invested
        if portfolio_balance:
            btc_percentage = round((user_btc_balance / portfolio_balance) * 100, 2)
            usd_percentage = round((usd_balance / portfolio_balance) * 100, 2)
        else:
            btc_percentage = 0
            usd_percentage = 0
        # Display the transaction history of the logged in user
        transaction = Transactions.objects.all().filter(
            user=request.user).order_by('transaction_date').reverse()

        # Insert Commas into display items
        btc_price = (
            '{:,.2f}'.format(bitcoin_price)
            if bitcoin_price is not None
            else 'Unavailable'
        )
        user_usd_balance = '{:,.2f}'.format(usd_balance)
        user_btc_balance = '{:,.2f}'.format(user_btc_balance)
        portfolio_balance = '{:,.2f}'.format(portfolio_balance)
        
        update.x = {'user_usd_balance': user_usd_balance,
                    'bitcoin_balance': bitcoin_balance,
                    'btc_price': btc_price,
                    'user_btc_balance': user_btc_balance,
                    'portfolio_balance': portfolio_balance,
                    'btc_percentage': btc_percentage,
                    'usd_percentage': usd_percentage,
                    'transaction': transaction,
                    'symbol': market_data}
        
        return update.x

    return render(request, 'app1/pages/DASHBOARD.html', {'update': update, 
                                                         'message': message})
                   

def quotes(request):
    quote = 'BTC'
    crypto = {}
    multi_market_data = {}

    # Get quote from user input
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        try:
            crypto = symbol()
        except (requests.RequestException, RuntimeError, ValueError):
            crypto = {}

    # API request
    def get_daily_crypto(symbol):
        coin_ids = {
            'BTC': 'bitcoin',
            'DASH': 'dash',
            'ETH': 'ethereum',
            'LTC': 'litecoin',
        }
        coin_id = coin_ids.get(symbol.upper())
        if coin_id is None:
            raise ValueError(f'Unsupported cryptocurrency: {symbol}')

        url = (
            f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
            '?vs_currency=usd&days=90&interval=daily'
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        payload = response.json()

        prices = payload.get('prices', [])
        if not prices:
            raise RuntimeError('No cryptocurrency history was returned.')

        dataframe = pd.DataFrame(prices, columns=['timestamp', 'price'])
        dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='ms')
        dataframe['high'] = dataframe['price']
        dataframe['low'] = dataframe['price']
        return dataframe

    # Display time series chart
    # Time series chart
    def get_crypto_daily_line_chart():
        df = get_daily_crypto(quote)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['high'], name=quote + " High",
                    line_color='deepskyblue'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['low'], name=quote + " Low",
                    line_color='dimgray'))
        fig.update_layout(title_text=quote,
                        xaxis_rangeslider_visible=True,
                        xaxis_title='Date',
                        yaxis_title='Price (USD)',
                        xaxis_range=['2019-07-01', timezone.datetime.now()],)
        return fig

    chart_error = ''
    try:
        chart = dcc.Graph(figure=get_crypto_daily_line_chart())
        quotes_dash_app.layout = html.Div(children=[html.Div(chart)])
    except (requests.RequestException, RuntimeError, ValueError):
        chart_error = (
            'Historical market data is temporarily unavailable. '
            'Please try again in a few minutes.'
        )
        quotes_dash_app.layout = html.Div(
            children=[html.Div(chart_error, className='alert alert-warning')]
        )

    return render(request, 'app1/pages/quotes.html', {'crypto': crypto, 
                                                      'mc_symbol': multi_market_data,
                                                      'chart_error': chart_error})


def crypto_news(request):
    news_data = news()
    return render(request, 'app1/pages/crypto_news.html', {'news': news_data})


def account(request):
    # Get BTC Price
    bitcoin_price = None
    market_data = {
        'DISPLAY': {
            'BTC': {
                'USD': {
                    'FROMSYMBOL': 'BTC',
                }
            }
        }
    }
    market_error = ''
    try:
        bitcoin_price = float(get_btc())
        market_data = symbol(bitcoin_price)
    except (requests.RequestException, RuntimeError, ValueError):
        market_error = (
            'Live BTC market data is temporarily unavailable. '
            'Portfolio values may be incomplete.'
        )

    # Get user BTC and USD balance from db
    usd_balance = float(request.user.account.usd_balance)
    bitcoin_balance = float(request.user.account.bitcoin_balance)

    message = '* Reset will delete the transactions history...'

    if request.method == 'POST':
        checkbox = request.POST['checkbox']
        if checkbox == 'true':
            # Update user account balances
            UPDATE_BTC = 0
            UPDATE_USD = 50000

            # Update the Database
            x = request.user.account
            x.bitcoin_balance = UPDATE_BTC
            x.usd_balance = UPDATE_USD
            x.save()

            # Delete user transaction history
            y = Transactions.objects.all().filter(user=request.user)
            y.delete()

            # Create Transaction Table Entry
            Transactions.objects.create(user_id=request.user.id,
                                        transaction_usd_price=0,
                                        transaction_type='RESET',
                                        transaction_date=timezone.datetime.now(),
                                        transaction_btc_quantity=0,
                                        transaction_total_usd_price=0)
            
            return redirect(account)
        else:
            message = "Check the 'Reset Accout' checkbox to Reset account balances..."

    # Calculate the USD value of the user's BTC
    effective_price = bitcoin_price or 0
    user_btc_balance = round((bitcoin_balance * effective_price), 2)
    # Calculate the total portfolio balance in USD
    portfolio_balance = user_btc_balance + usd_balance
    # Calculate the percantage of the portfolio invested
    if portfolio_balance:
        btc_percentage = round((user_btc_balance / portfolio_balance) * 100, 2)
        usd_percentage = round((usd_balance / portfolio_balance) * 100, 2)
    else:
        btc_percentage = 0
        usd_percentage = 0
    # Calculate the change
    change = round(portfolio_balance + (50000 * -1),2)
    print(change)
    
    # Display the transaction history of the logged in user
    transaction = Transactions.objects.all().filter(
        user=request.user).order_by('transaction_date').reverse()

    # Insert Commas into display items
    user_usd_balance = '{:,.2f}'.format(usd_balance)
    user_btc_value = '{:,.2f}'.format(user_btc_balance)
    portfolio_balance = '{:,.2f}'.format(portfolio_balance)

    return render(request, 'app1/pages/account.html', {'symbol': market_data,
                                                       'btc_percentage': btc_percentage, 
                                                       'bitcoin_balance': bitcoin_balance, 
                                                       'usd_percentage': usd_percentage,
                                                       'usd_balance': usd_balance, 
                                                       'user_usd_balance': user_usd_balance,
                                                       'user_btc_balance': user_btc_balance,
                                                       'user_btc_value': user_btc_value,
                                                       'portfolio_balance': portfolio_balance,
                                                       'change': change,
                                                       'transaction': transaction,
                                                       'message': message,
                                                       'market_error': market_error})
