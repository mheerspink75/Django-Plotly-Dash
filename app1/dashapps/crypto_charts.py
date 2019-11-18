import pandas as pd
import pandas_datareader.data as web
from pandas_datareader import data
import datetime
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash


API_KEY = 'ALPHAVANTAGE_API_KEY'

app = DjangoDash('crypto-charts')


app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    html.Div(dcc.Input(id='input', value='BTC', type='text', debounce=True)),
    html.Div(id='output-graph'),
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)


def update_value(input_data):
    df = web.DataReader([(input_data + "/USD"),
                    ("USD/" + input_data)],
                    "av-forex", api_key=API_KEY).reset_index()


    crypto_table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records')) 

    ##### DIGITAL_CURRENCY_DAILY #####
    def get_daily_crypto(input_data):
        daily = 'DIGITAL_CURRENCY_DAILY'
        print('Currently pulling: ', input_data, daily)

        CRYPTO_DAILY_OHLC = 'https://www.alphavantage.co/query?function=' + daily + '&symbol=' + input_data + '&market=USD&apikey=' + API_KEY + '&datatype=csv'

        CRYPTO_DAILY_TIME_SERIES = pd.read_csv(CRYPTO_DAILY_OHLC)
        return CRYPTO_DAILY_TIME_SERIES
    print(get_daily_crypto(input_data))


    def get_crypto_daily_OHLC_chart():
        df = get_daily_crypto(input_data)
        fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                    open=df['open (USD)'], high=df['high (USD)'],
                    low=df['low (USD)'], close=df['close (USD)'],
                    increasing_line_color='cyan',
                    decreasing_line_color='gray'),
                        ])

        fig.update_layout(title_text=(input_data.upper() + ' (USD)'),
                    xaxis_rangeslider_visible=True,
                    xaxis_title='Date',
                    yaxis_title='Price (USD)',
                    xaxis_range=['2019-07-01', datetime.datetime.now()],
                    height=600)

        return fig

    crypto_graph = dcc.Graph(figure=(get_crypto_daily_OHLC_chart()))

    return html.Div([crypto_graph, crypto_table])










