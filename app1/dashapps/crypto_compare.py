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

