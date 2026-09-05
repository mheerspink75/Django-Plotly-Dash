import pandas as pd

API_KEY = 'ALPHAVANTAGE_API_KEY'

symbol = ''
datatype = 'csv'  # ['json', 'csv']


##### TIME_SERIES_INTRADAY #####
def get_intraday_time_series(symbol):
    intraday = 'TIME_SERIES_INTRADAY'
    intraday_interval = '1min'  # ['1min', '5min', '15min', '30min', '60min']
    print('Currently pulling: ', symbol, intraday, intraday_interval)

    INTRADAY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + intraday) + \
        ('&symbol=' + symbol) + ('&interval=' + intraday_interval) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    INTRADAY_TIME_SERIES = pd.read_csv(INTRADAY_OHLC).head(1)
    return INTRADAY_TIME_SERIES


##### TIME_SERIES_DAILY #####
def get_daily_time_series(symbol):
    daily = 'TIME_SERIES_DAILY'
    print('Currently pulling: ', symbol, daily)

    DAILY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + daily) + \
        ('&symbol=' + symbol) + ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    DAILY_TIME_SERIES = pd.read_csv(DAILY_OHLC)
    return DAILY_TIME_SERIES


##### TIME_SERIES_WEEKLY #####
def get_weekly_time_series(symbol):
    weekly = 'TIME_SERIES_WEEKLY'
    print('Currently pulling: ', symbol, weekly)

    WEEKLY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + weekly) + \
        ('&symbol=' + symbol) + ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    WEEKLY_TIME_SERIES = pd.read_csv(WEEKLY_OHLC)
    return WEEKLY_TIME_SERIES


##### TIME_SERIES_MONTHLY #####
def get_monthly_time_series(symbol):
    monthly = 'TIME_SERIES_MONTHLY'
    print('Currently pulling: ', symbol, monthly)

    MONTHLY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + monthly) + \
        ('&symbol=' + symbol) + ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    MONTHLY_TIME_SERIES = pd.read_csv(MONTHLY_OHLC)
    return MONTHLY_TIME_SERIES


############################################
## print(get_intraday_time_series(symbol))##
## print(get_daily_time_series(symbol))#####
## print(get_weekly_time_series(symbol))####
## print(get_monthly_time_series(symbol))###
############################################
