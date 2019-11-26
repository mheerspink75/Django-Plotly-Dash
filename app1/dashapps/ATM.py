import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Sign
import pandas as pd
from collections import OrderedDict
from django_plotly_dash import DjangoDash

from django.contrib.auth.models import User
from django.db import models
from app1.models import Account



app = DjangoDash('ATM')


date = datetime.datetime.now()

account_balance = pd.DataFrame(OrderedDict([
    ('date', [Account.objects.get(pk=1).account_date]),
    ('amount', [Account.objects.get(pk=1).account_balance]),
    ('Username', [Account.objects.get(pk=1).user.username]),
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
            'id': 'Username',
            'name': 'Username',
            'type': 'text',
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
    ('amount', [Account.objects.get(pk=1).cash_balance]),
   # ('change', [0]),
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
            },
        ], 
    )
)


transaction_history = pd.DataFrame(OrderedDict([
    ('date', [Account.objects.get(pk=1).transaction_date]),
    ('transaction', [Account.objects.get(pk=1).transaction_type]),
    ('amount', [Account.objects.get(pk=1).transaction_amount]),
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
    html.Div(id='output-container-button')
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return '{}'.format(
        value,
        n_clicks
    )

