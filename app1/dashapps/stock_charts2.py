import pandas as pd
import pandas_datareader.data as web
from pandas_datareader import data
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash


app = DjangoDash('stock-chart')


##### YAHOO FINANCE #####
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime.now()

app.layout = html.Div(children=[
    html.Div(children='''Symbol to graph:'''),
    dcc.Input(id='my-id', value='AAPL', type='text', debounce=True),
    html.Div([html.Div(id='my-div')])
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)


def update_output_div(input_value):
    x = input_value.upper()
    df = data.DataReader(x, 'yahoo')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=df.High,
                             name=(input_value.upper() + " High"),
                             line_color='deepskyblue'))

    fig.add_trace(go.Scatter(x=df.index, y=df.Low,
                             name=(input_value.upper() + " Low"),
                             line_color='dimgray'))

    fig.update_layout(title=input_value.upper(),
                      font_size=15,
                      xaxis_rangeslider_visible=True,
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_range=[start, end],)

    OHLC_chart = dcc.Graph(figure=(fig))

    return html.Div(children=[html.Div(OHLC_chart)])
