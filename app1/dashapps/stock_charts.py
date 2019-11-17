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


##### ALPHAVANTAGE #####
API_KEY = 'ALPHAVANTAGE_API_KEY'
datatype = 'csv'  # ['json', 'csv']

##### YAHOO FINANCE #####
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime.now()


app = DjangoDash('stock-chart')


app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    html.Div(dcc.Input(id='input', value='AAPL', type='text', debounce=True)),
    html.Div(id='output-graph'),
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    ##### YAHOO FINANCE #####
    df = data.DataReader(input_data, 'yahoo')
    # print(df.tail(1))

    ###### ALPHAVANTAGE TIME_SERIES_INTRADAY ######
    def get_intraday_time_series(input_data):
        intraday = 'TIME_SERIES_INTRADAY'
        # ['1min', '5min', '15min', '30min', '60min']
        intraday_interval = '1min'
        #print('Currently pulling: ', input_data, intraday, intraday_interval)

        INTRADAY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + intraday) + \
            ('&symbol=' + input_data) + ('&interval=' + intraday_interval) + \
            ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

        INTRADAY_TIME_SERIES = pd.read_csv(INTRADAY_OHLC)
        return INTRADAY_TIME_SERIES

    QUOTE_SEARCH = web.get_quote_av(
        input_data, api_key=(API_KEY)).reset_index()
    # print(QUOTE_SEARCH.tail())

    OHLC_INTRADAY_QUOTE = get_intraday_time_series(input_data)
    # print(OHLC_INTRADAY_QUOTE.tail())

    QUOTE_table = dash_table.DataTable(
        id='Quote_table',
        columns=[{"name": i, "id": i} for i in QUOTE_SEARCH.columns],
        data=QUOTE_SEARCH.tail(1).to_dict('records'))

    OHLC_table = dash_table.DataTable(
        id='OHLC_table',
        columns=[{"name": i, "id": i} for i in OHLC_INTRADAY_QUOTE.columns],
        data=OHLC_INTRADAY_QUOTE.head(1).to_dict('records'))

    OHLC_INTRADAY_GRAPH = dcc.Graph(figure=go.Figure(
                                    data=[go.Candlestick(
                                        x=OHLC_INTRADAY_QUOTE.timestamp,
                                        open=OHLC_INTRADAY_QUOTE['open'],
                                        high=OHLC_INTRADAY_QUOTE['high'],
                                        low=OHLC_INTRADAY_QUOTE['low'],
                                        close=OHLC_INTRADAY_QUOTE['close'],
                                        increasing_line_color='cyan',
                                        decreasing_line_color='gray')]))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.Open, name=(input_data.upper() + " Open"),
                             line_color='lightskyblue'))

    fig.add_trace(go.Scatter(x=df.index, y=df.High, name=(input_data.upper() + " High"),
                             line_color='lightsteelblue'))

    fig.add_trace(go.Scatter(x=df.index, y=df.Low, name=(input_data.upper() + " Low"),
                             line_color='lightgray'))

    fig.add_trace(go.Scatter(x=df.index, y=df.Close, name=(input_data.upper() + " Close"),
                             line_color='skyblue'))

    fig.update_layout(title=input_data.upper(),
                      font_size=15,
                      xaxis_rangeslider_visible=True,
                      yaxis_title='Price (USD)',
                      xaxis_range=[start, end],
                      height=700)

    OHLC_chart = dcc.Graph(figure=(fig))

    return html.Div([QUOTE_table, OHLC_chart, OHLC_table, OHLC_INTRADAY_GRAPH, QUOTE_table])
