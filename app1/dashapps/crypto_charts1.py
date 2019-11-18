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

app = DjangoDash('crypto-table')




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
    df = web.DataReader(input_data + "/USD", "av-forex", api_key=API_KEY).reset_index()
    print(df)

    return dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)










