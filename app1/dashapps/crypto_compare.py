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
    