import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import dash_table
import pandas as pd
import pandas_datareader.data as web
from django_plotly_dash import DjangoDash

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']

def get_forex():
    return web.DataReader(["USD/BTC", "BTC/USD"], "av-forex", api_key=API_KEY).reset_index()
df = get_forex()


app = DjangoDash('dashtable')

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)













