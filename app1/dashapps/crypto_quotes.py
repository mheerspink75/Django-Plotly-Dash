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
import json

app = DjangoDash('crypto-quotes')

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']

# Get BTC Price Data
def get_btc_price():
    bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    bitcoin_price = json.loads(bitcoin_price_request.content)
    return float(bitcoin_price['USD'])

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
    fig.update_layout(title_text=('BTC (USD)' + '  ' + '$' + str(get_btc_price())),
                      xaxis_rangeslider_visible=True,
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_range=['2018-01-01', datetime.datetime.now()],)
    return fig


chart = dcc.Graph(figure=(get_crypto_daily_line_chart()))
app.layout = html.Div(children=[html.Div(chart)])
