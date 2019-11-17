import pandas as pd
from API_KEYS import ALPHAVANTAGE_API_KEY

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']

SMA = 'https://www.alphavantage.co/query?' + 'function=SMA' + '&symbol=' + \
    (symbol + market) + '&interval=weekly' + '&time_period=10' + \
    '&series_type=open' + '&apikey=' + (API_KEY)
print(pd.read_json(SMA))
