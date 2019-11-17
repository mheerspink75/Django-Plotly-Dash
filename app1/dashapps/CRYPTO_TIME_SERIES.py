import pandas as pd
from API_KEYS import ALPHAVANTAGE_API_KEY

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = 'BTC'
market = 'USD'

datatype = 'csv'  # ['json', 'csv']


##### DIGITAL_CURRENCY_DAILY #####
def get_daily_crypto(symbol):
    daily = 'DIGITAL_CURRENCY_DAILY'
    print('Currently pulling: ', symbol, daily)

    CRYPTO_DAILY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + daily) + \
        ('&symbol=' + symbol) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_DAILY_TIME_SERIES = pd.read_csv(CRYPTO_DAILY_OHLC)
    return CRYPTO_DAILY_TIME_SERIES


##### DIGITAL_CURRENCY_WEEKLY #####
def get_weekly_crypto(symbol):
    weekly = 'DIGITAL_CURRENCY_WEEKLY'
    print('Currently pulling: ', symbol, weekly)

    CRYPTO_WEEKLY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + weekly) + \
        ('&symbol=' + symbol) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_WEEKLY_TIME_SERIES = pd.read_csv(CRYPTO_WEEKLY_OHLC)
    return CRYPTO_WEEKLY_TIME_SERIES


##### DIGITAL_CURRENCY_MONTHLY #####
def get_monthly_crypto(symbol):
    monthly = 'DIGITAL_CURRENCY_MONTHLY'
    print('Currently pulling: ', symbol, monthly)

    CRYPTO_MONTHLY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + monthly) + \
        ('&symbol=' + symbol) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_MONTHLY_TIME_SERIES = pd.read_csv(CRYPTO_MONTHLY_OHLC)
    return CRYPTO_MONTHLY_TIME_SERIES


####################################
##print(get_daily_crypto(symbol))###
##print(get_weekly_crypto(symbol))##
##print(get_monthly_crypto(symbol))#
####################################
