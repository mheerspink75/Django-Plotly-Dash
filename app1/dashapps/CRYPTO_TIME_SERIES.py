import pandas as pd
from API_KEYS import ALPHAVANTAGE_API_KEY
import urllib.request
import requests
import json

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']


##### DIGITAL_CURRENCY_DAILY #####
def get_daily_crypto(symbol):
    daily = 'DIGITAL_CURRENCY_DAILY'
    #print('Currently pulling: ', symbol, daily)

    CRYPTO_WEEKLY_OHLC = ('https://www.alphavantage.co/query?' + 'function=' + daily + '&symbol=' + symbol + '&market=' + market + '&apikey=' + API_KEY + '&datatype=' + datatype)
    CRYPTO_DAILY_TIME_SERIES = pd.read_csv(CRYPTO_DAILY_OHLC)
    return CRYPTO_DAILY_TIME_SERIES


##### DIGITAL_CURRENCY_WEEKLY #####
def get_weekly_crypto(symbol):
    weekly = 'DIGITAL_CURRENCY_WEEKLY'
    #print('Currently pulling: ', symbol, weekly)

    CRYPTO_WEEKLY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + weekly) + \
        ('&symbol=' + symbol) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_WEEKLY_TIME_SERIES = pd.read_csv(CRYPTO_WEEKLY_OHLC)
    return CRYPTO_WEEKLY_TIME_SERIES


##### DIGITAL_CURRENCY_MONTHLY #####
def get_monthly_crypto(symbol):
    monthly = 'DIGITAL_CURRENCY_MONTHLY'
    #print('Currently pulling: ', symbol, monthly)

    CRYPTO_MONTHLY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + monthly) + \
        ('&symbol=' + symbol) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_MONTHLY_TIME_SERIES = pd.read_csv(CRYPTO_MONTHLY_OHLC)
    return CRYPTO_MONTHLY_TIME_SERIES

# Get BTC Full Data
coins = 'BTC'
symbol_request = requests.get(
    'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coins + '&tsyms=USD')
symbol = json.loads(symbol_request.content)
#print(symbol['DISPLAY']['BTC']['USD']['FROMSYMBOL'])
#print(symbol['DISPLAY']['BTC']['USD']['PRICE'])

minute_time_series = pd.read_csv('https://min-api.cryptocompare.com/data/histo/minute/daily?fsym=BTC&tsym=USD&date=2019-07-21&api_key=f70ce7c70b85a5e9105dcd3d2c94719981d4aad92cb8febd824d1c0fa0f0568d')
#print(minute_time_series)

####################################
##print(get_daily_crypto(symbol))###
##print(get_weekly_crypto(symbol))##
##print(get_monthly_crypto(symbol))#
####################################
