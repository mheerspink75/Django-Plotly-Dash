from pandas_datareader import data
import datetime
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash


start = datetime.datetime(2017, 1, 1)
end = datetime.datetime.now()


app = DjangoDash('dashinputtable')


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
    df = data.DataReader(input_data, 'yahoo')
    #print(df.tail(1))

    OHLC_table = dash_table.DataTable(
    id='OHLC_table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.tail(1).to_dict('records')) 

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.High, name=(input_data.upper() + " High"),
                         line_color='deepskyblue'))
    
    fig.add_trace(go.Scatter(x=df.index, y=df.Low, name=(input_data.upper() + " Low"),
                         line_color='lightgray'))

    fig.update_layout(title=input_data.upper(),
                  font_size=15,
                  xaxis_rangeslider_visible=True,
                  xaxis_title='Date',
                  yaxis_title='Price (USD)',
                  xaxis_range=[start, end],
                  height=700)

    OHLC_chart = dcc.Graph(figure=(fig))
        

    return html.Div([OHLC_chart, OHLC_table])

     