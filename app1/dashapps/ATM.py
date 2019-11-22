import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Sign
import pandas as pd
from collections import OrderedDict


app = dash.Dash(__name__)

date = datetime.datetime.now()

account_balance = pd.DataFrame(OrderedDict([
    ('date', [date]),
    ('amount', [1092000]),
    ('change', [0.143]),
]))


account_balance_table = html.Div(
    dash_table.DataTable(
        id='account_balance',
        data=account_balance.to_dict('rows'),
        columns=[{
            'id': 'date',
            'name': 'Date',
                    'type': 'text'
        }, {
            'id': 'change',
            'name': 'Change (%)',
            'type': 'numeric',
            'format': FormatTemplate.percentage(1).sign(Sign.positive)
        }, {
            'id': 'amount',
            'name': 'Account Balance ($)',
            'type': 'numeric',
            'format': FormatTemplate.money(0)
        },
        ],
    )
)


cash_balance = pd.DataFrame(OrderedDict([
    ('amount', [1092000]),
    ('change', [0.143]),
]))


cash_balance_table = html.Div(
    dash_table.DataTable(
        id='cash_balance',
        data=cash_balance.to_dict('rows'),
        columns=[{
            'id': 'amount',
            'name': 'Cash Balance ($)',
                    'type': 'numeric',
                    'format': FormatTemplate.money(0)
        }, {
            'id': 'change',
            'name': 'Change (%)',
            'type': 'numeric',
            'format': FormatTemplate.percentage(1).sign(Sign.positive)
        },
        ],     style_cell_conditional=[
            {'if': {'column_id': 'amount'},
             'width': '57%'},
            {'if': {'column_id': 'change'},
             'width': '30%'},
        ]
    )
)


transaction_history = pd.DataFrame(OrderedDict([
    ('date', [date]),
    ('transaction', ['null']),
    ('amount', [0]),
    ('change', [0]),
]))


transaction_history_table = html.Div(
    dash_table.DataTable(
        id='transaction_history',
        data=transaction_history.to_dict('rows'),
        columns=[{
            'id': 'date',
            'name': 'Transaction Date',
                    'type': 'text'
        }, {
            'id': 'transaction',
            'name': 'Transaction',
            'type': 'text',
        }, {
            'id': 'amount',
            'name': 'Amount ($)',
            'type': 'numeric',
            'format': FormatTemplate.money(0)
        },
        ]
    )
)


radio = dcc.RadioItems(
    options=[
        {'label': 'Deposit', 'value': 'NYC'},
        {'label': 'Withdrawl', 'value': 'MTL'},
    ],
    value='MTL',
    labelStyle={'display': 'inline-block'}
)


app.layout = html.Div([
    account_balance_table,
    cash_balance_table,
    radio,
    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button'),
    transaction_history_table,
    html.Div(id='output-container-button',
             children='Enter a value and press submit')
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}"'.format(
        value,
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(debug=True)
