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
    bitquote_price = float(get_btc())

    # Error messages
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
            USD_SALE_PRICE = (BUY_BTC * bitquote_price)
            # Update BTC Balance Quantity
            UPDATE_BTC = round(BUY_BTC + bitcoin_balance, 2)
            # Update USD Balance
            UPDATE_USD = round(usd_balance - USD_SALE_PRICE, 2)

        # Calculate USD Trade
        if inlineRadioOptions == 'TRADE_USD':
            if BUY_SELL == 'BUY':
                BUY_BTC = BUY_BTC * -1
            # USD Value of sale
            USD_SALE_PRICE = BUY_BTC * -1
            # Update USD Balance
            UPDATE_USD = round(BUY_BTC + usd_balance, 2)
            # Calculate the BTC Quantity
            BUY_BTC = round((USD_SALE_PRICE / bitquote_price), 2)
            # Update BTC Balance Quantity
            UPDATE_BTC = BUY_BTC + bitcoin_balance

        # Update the Database
        x = request.user.account
        x.bitcoin_balance = UPDATE_BTC
        x.usd_balance = UPDATE_USD

        # Check for insufficient funds
        if x.usd_balance >= 0 and x.bitcoin_balance >= 0:
            # Create Transaction Table Entry
            Transactions.objects.create(user_id=request.user.id,
                                        transaction_usd_price=bitquote_price,
                                        transaction_type=BUY_SELL,
                                        transaction_date=timezone.datetime.now(),
                                        transaction_btc_quantity=BUY_BTC,
                                        transaction_total_usd_price=(USD_SALE_PRICE * -1))
            x.save()
            return redirect(DASHBOARD)
        else:
            error = 'Insufficient funds...\n  *** Sale Denied! ***'

    # Prepare
    def update():
        # Calculate the USD value of the user's BTC
        user_btc_balance = round((bitcoin_balance * bitquote_price), 2)
        # Calculate the total portfolio balance in USD
        portfolio_balance = round(user_btc_balance + usd_balance, 2)
        # Calculate the percantage of the portfolio invested
        btc_percentage = round((user_btc_balance / portfolio_balance) * 100, 2)
        usd_percentage = round((usd_balance / portfolio_balance) * 100, 2)
        # Display the transaction history of the logged in user
        transaction = Transactions.objects.all().filter(
            user=request.user).order_by('transaction_date').reverse()

        # Insert Commas into display items
        btc_price = '{:,.2f}'.format(bitquote_price)
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
                                                         'error': error})
                   

def quotes(request):
    quote = 'BTC'
    error = ''

    # Get quote from user input
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto = json.loads(crypto_request.content)
    else:
        crypto = symbol
        error = '*** ERROR! ***'

    # API request
    def get_daily_crypto(symbol):
        API_KEY = 'ALPHAVANTAGE_API_KEY'
        market = 'USD'
        datatype = 'csv'  # ['json', 'csv']

        ##### ALPHAVANTAGE API DIGITAL_CURRENCY_DAILY #####
        daily = 'DIGITAL_CURRENCY_DAILY'
        print('Currently pulling: ', quote, daily)
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
                                                      'mc_symbol': mc_symbol,
                                                      'error': error})


def crypto_news(request):
    return render(request, 'app1/pages/crypto_news.html', {'news': news})
