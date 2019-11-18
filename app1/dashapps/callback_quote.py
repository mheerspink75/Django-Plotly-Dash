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
    dff = df.tail(1).reset_index()
    dfff = data.DataReader(x, 'yahoo', start='2019-10-1', end=datetime.datetime.now())


    table = dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in dff.columns], data=dff.to_dict('records'))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.Open, 
                            name=(input_value.upper() + " Open"),
                            line_color='lightskyblue'))

    fig.add_trace(go.Scatter(x=df.index, y=df.High, 
                             name=(input_value.upper() + " High"),
                             line_color='lightsteelblue'))

    fig.add_trace(go.Scatter(x=df.index, y=df.Low, 
                             name=(input_value.upper() + " Low"),
                             line_color='lightgray'))

    fig.add_trace(go.Scatter(x=df.index, y=df.Close, 
                            name=(input_value.upper() + " Close"),
                            line_color='skyblue'))

    fig.update_layout(title=input_value.upper(),
                      font_size=15,
                      xaxis_rangeslider_visible=True,
                      yaxis_title='Price (USD)',
                      xaxis_range=[start, end],
                      height=700)

    OHLC_chart = dcc.Graph(figure=(fig))

    OHLC_candlestick = dcc.Graph(figure=go.Figure(
                                data=[go.Candlestick(
                                    x=dfff.index,
                                    open=dfff['Open'],
                                    high=dfff['High'],
                                    low=dfff['Low'],
                                    close=dfff['Close'],
                                    increasing_line_color='cyan',
                                    decreasing_line_color='gray')]))

    return (table, OHLC_chart, table, OHLC_candlestick, table)

if __name__ == '__main__':
    app.run_server(debug=True)