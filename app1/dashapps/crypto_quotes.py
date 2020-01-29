import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime
import dash_table
import pandas as pd
import pandas_datareader.data as web
from django_plotly_dash import DjangoDash
import requests


app = DjangoDash('crypto-quotes')

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']

#### COIN_MARKETCAP_API ####

TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
def get_latest_crypto_price( crypto ):
    response = requests.get(TICKER_API_URL+crypto)
    response_json = response.json()
    # Convert the price to a floating point number
    return float(response_json[0]['price_usd'])

def BTC_PRICE():
    return str(get_latest_crypto_price( 'bitcoin'))

##### ALPHAVANTAGE API DIGITAL_CURRENCY_DAILY #####

def get_daily_crypto(symbol):
    daily = 'DIGITAL_CURRENCY_DAILY'
    #print('Currently pulling: ', symbol, daily)

    CRYPTO_DAILY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + daily) + \
        ('&symbol=' + symbol) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_DAILY_TIME_SERIES = pd.read_csv(CRYPTO_DAILY_OHLC)
    return CRYPTO_DAILY_TIME_SERIES


def get_crypto_daily_line_chart():
    df = get_daily_crypto(symbol)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.timestamp, y=df['high (USD)'], name="BTC High (USD)",
                             line_color='deepskyblue'))

    fig.add_trace(go.Scatter(x=df.timestamp, y=df['low (USD)'], name="BTC Low (USD)",
                             line_color='dimgray'))

    fig.update_layout(title_text=('BTC (USD)' + '  ' + '$' + BTC_PRICE()),
                      xaxis_rangeslider_visible=True,
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_range=['2018-01-01', datetime.datetime.now()],)
    return fig


chart = dcc.Graph(figure=(get_crypto_daily_line_chart()))


app.layout = html.Div(children=[html.Div(chart)])
