import pandas as pd
import pandas_datareader.data as web
from API_KEYS import ALPHAVANTAGE_API_KEY

API_KEY = 'ALPHAVANTAGE_API_KEY'

input_data = input('Enter a symbol: ').upper()

def get_forex():
    return web.DataReader(["USD/BTC", "BTC/USD"], "av-forex", api_key=API_KEY).reset_index()
#print(get_forex())

def get_input_data():
    return web.DataReader(["USD/" + input_data, input_data + "/USD"], "av-forex", api_key=API_KEY).reset_index()
#print(get_input_data())

#### REALTIME #################################################################################################################################
# x = pd.read_json('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=' + 'APIKEY')
# y = pd.read_json('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=BTC&apikey=' + 'APIKEY')
# print(x)
