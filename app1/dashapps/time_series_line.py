import pandas as pd
import plotly.graph_objects as go
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from API_KEYS import ALPHAVANTAGE_API_KEY

app = dash.Dash(__name__)

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']

##### DIGITAL_CURRENCY_DAILY #####
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

    fig.update_layout(title_text='Time series - BTC (USD)',
                    xaxis_rangeslider_visible=True,
                    xaxis_title='Date',
                    yaxis_title='Price (USD)',
                    xaxis_range=['', datetime.datetime.now()],)
    return fig
    
def get_crypto_daily_OHLC_chart():
    df = get_daily_crypto(symbol)
    fig = go.Figure(data=[go.Ohlc(x=df['timestamp'],
                open=df['open (USD)'], high=df['high (USD)'],
                low=df['low (USD)'], close=df['close (USD)'])
                     ])

    fig.update_layout(title_text='Time series OHLC - BTC (USD)',
                xaxis_rangeslider_visible=False,
                xaxis_title='Date',
                yaxis_title='Price (USD)',
                xaxis_range=['2019-01-01', datetime.datetime.now()],)
    return fig

app.layout = dcc.Graph(figure=(get_crypto_daily_line_chart()))


if __name__ == '__main__':
    app.run_server(debug=True)