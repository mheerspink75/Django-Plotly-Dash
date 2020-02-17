from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from app1.models import Account, Transactions
import requests
import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from app1.dashapps.crypto_compare import get_btc, symbol, news, mc_symbol


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
    bitcoin_price = float(get_btc())

    # message messages
    message = ''

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

    # Prepare
    def update():
        # Calculate the USD value of the user's BTC
        user_btc_balance = round((bitcoin_balance * bitcoin_price), 2)
        # Calculate the total portfolio balance in USD
        portfolio_balance = user_btc_balance + usd_balance
        # Calculate the percantage of the portfolio invested
        btc_percentage = round((user_btc_balance / portfolio_balance) * 100, 2)
        usd_percentage = round((usd_balance / portfolio_balance) * 100, 2)
        # Display the transaction history of the logged in user
        transaction = Transactions.objects.all().filter(
            user=request.user).order_by('transaction_date').reverse()

        # Insert Commas into display items
        btc_price = '{:,.2f}'.format(bitcoin_price)
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
                    'symbol': symbol}
        
        return update.x

    return render(request, 'app1/pages/DASHBOARD.html', {'update': update, 
                                                         'message': message})
                   

def quotes(request):
    quote = 'BTC'

    # Get quote from user input
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        crypto = symbol

    # API request
    def get_daily_crypto(symbol):
        API_KEY = 'ALPHAVANTAGE_API_KEY'
        market = 'USD'
        datatype = 'csv'  # ['json', 'csv']

        ##### ALPHAVANTAGE API DIGITAL_CURRENCY_DAILY #####
        daily = 'DIGITAL_CURRENCY_DAILY'
        CRYPTO_DAILY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + daily) + \
            ('&symbol=' + quote) + ('&market=' + market) + \
            ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

        CRYPTO_DAILY_TIME_SERIES = pd.read_csv(CRYPTO_DAILY_OHLC)
        return CRYPTO_DAILY_TIME_SERIES

    # Display time series chart
    app = DjangoDash('crypto-chart2')

    # Time series chart
    def get_crypto_daily_line_chart():
        df = get_daily_crypto(symbol)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.timestamp, y=df['high (USD)'], name=quote + " High",
                                line_color='deepskyblue'))
        fig.add_trace(go.Scatter(x=df.timestamp, y=df['low (USD)'], name=quote + " Low",
                                line_color='dimgray'))
        fig.update_layout(title_text=quote,
                        xaxis_rangeslider_visible=True,
                        xaxis_title='Date',
                        yaxis_title='Price (USD)',
                        xaxis_range=['2019-07-01', timezone.datetime.now()],)
        return fig

    chart = dcc.Graph(figure=(get_crypto_daily_line_chart()))
    app.layout = html.Div(children=[html.Div(chart)])

    return render(request, 'app1/pages/quotes.html', {'crypto': crypto, 
                                                      'mc_symbol': mc_symbol})


def crypto_news(request):
    return render(request, 'app1/pages/crypto_news.html', {'news': news})


def account(request):
    # Get BTC Price
    bitcoin_price = float(get_btc())
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
    user_btc_balance = round((bitcoin_balance * bitcoin_price), 2)
    # Calculate the total portfolio balance in USD
    portfolio_balance = user_btc_balance + usd_balance
    # Calculate the percantage of the portfolio invested
    btc_percentage = round((user_btc_balance / portfolio_balance) * 100, 2)
    usd_percentage = round((usd_balance / portfolio_balance) * 100, 2)
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

    return render(request, 'app1/pages/account.html', {'symbol': symbol,
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
                                                       'message': message})
