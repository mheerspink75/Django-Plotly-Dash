import pandas as pd
from pandas_datareader import data
import plotly.graph_objects as go
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from API_KEYS import ALPHAVANTAGE_API_KEY

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = ''
datatype = 'csv'  # ['json', 'csv']


##### TIME_SERIES_INTRADAY #####
def get_intraday_time_series(symbol):
    intraday = 'TIME_SERIES_INTRADAY'
    intraday_interval = '1min'  # ['1min', '5min', '15min', '30min', '60min']
    print('Currently pulling: ', symbol, intraday, intraday_interval)

    INTRADAY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + intraday) + \
        ('&symbol=' + symbol) + ('&interval=' + intraday_interval) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    INTRADAY_TIME_SERIES = pd.read_csv(INTRADAY_OHLC)
    return INTRADAY_TIME_SERIES

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Input(id='input', value='AAPL', type='text', debounce=True),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_value(input_data):
    df = get_intraday_time_series(input_data)
    print(df)

    return dcc.Graph(figure=go.Figure(data=[go.Candlestick(
    x=df.timestamp,
    open=df['open'], high=df['high'],
    low=df['low'], close=df['close'],
    increasing_line_color= 'cyan', decreasing_line_color= 'gray'
)]))

if __name__ == '__main__':
    app.run_server(debug=True)
