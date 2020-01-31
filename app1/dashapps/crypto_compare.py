import requests
import json

# Get Bitcoin Price
bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
bitcoin_price = json.loads(bitcoin_price_request.content)

print(bitcoin_price['USD'])


#### COIN_MARKETCAP_API ####

TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
def get_latest_crypto_price( crypto ):
    response = requests.get(TICKER_API_URL+crypto)
    response_json = response.json()
    # Convert the price to a floating point number
    return float(response_json[0]['price_usd'])

def BTC_PRICE():
    return str(get_latest_crypto_price( 'bitcoin'))
print(BTC_PRICE)