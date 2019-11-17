import pandas_datareader.data as web
from API_KEYS import ALPHAVANTAGE_API_KEY

API_KEY = 'ALPHAVANTAGE_API_KEY'


def get_forex():
    return web.DataReader(["USD/BTC", "BTC/USD"], "av-forex", api_key=API_KEY)


print(get_forex())
