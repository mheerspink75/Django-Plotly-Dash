import requests
import json

# Get Bitcoin Price
def get_btc():
    bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    bitcoin_price = json.loads(bitcoin_price_request.content)
    bitcoin_price = bitcoin_price['USD']
    return bitcoin_price

# Get BTC Full Data
def symbol():
    symbol_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD')
    symbol = json.loads(symbol_request.content)
    return symbol

# Get News Feed
def news():
    news_request = requests.get(
        'https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    news = json.loads(news_request.content)
    return news

# Get Multiple Currency Full Data
def mc_symbol():
    multi_quote = 'BTC,ETH,BCH,ETC,XRP,BSV,EOS,LTC,TRX,OKB,BNB,DASH'
    mc_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + multi_quote + '&tsyms=USD')
    mc_symbol = json.loads(mc_request.content)
    return mc_symbol

# Get Time Series
def get_daily_crypto(symbol):
    quote = 'BTC'
    API_KEY = 'ALPHAVANTAGE_API_KEY'
    market = 'USD'
    datatype = 'csv'  # ['json', 'csv']

    ##### ALPHAVANTAGE API DIGITAL_CURRENCY_DAILY #####
    daily = 'DIGITAL_CURRENCY_DAILY'
    print('Currently pulling: ', quote, daily)
    CRYPTO_DAILY_OHLC = ('https://www.alphavantage.co/query?') + ('function=' + daily) + \
        ('&symbol=' + quote) + ('&market=' + market) + \
        ('&apikey=' + API_KEY) + ('&datatype=' + datatype)

    CRYPTO_DAILY_TIME_SERIES = pd.read_csv(CRYPTO_DAILY_OHLC)
    return CRYPTO_DAILY_TIME_SERIES




        
'''
def numbers():
    my_number = 4385893.38
    my_number_2 = 123456789.87
    list = [my_number, my_number_2]
    for member in list:
        form = '{:,.2f}'.format(member)
        return form

print(numbers())

my_number = 4385893.38
my_number_2 = 123456789.87
list = [my_number, my_number_2]
for member in list:
    form = '{:,.2f}'.format(member)
    print(form)

'''
'''
list = [0.34555, 0.2323456, 0.6234232, 0.45234234]
for member in list:
    form='{:.1%}'.format(member)


#my_string = '{:,.2f}'.format(my_number)
#print(my_string)
'''