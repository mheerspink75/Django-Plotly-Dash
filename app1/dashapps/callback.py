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


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Input(id='my-id', value='AAPL', type='text', debounce=True),
    html.Div([html.Div(id='my-div')])
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)

def update_output_div(input_value):
    x = input_value.upper()
    df = data.DataReader(x, 'yahoo').tail(1).reset_index()
    print(df)
    return (x, dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in df.columns], data=df.to_dict('records')))

if __name__ == '__main__':
    app.run_server(debug=True)