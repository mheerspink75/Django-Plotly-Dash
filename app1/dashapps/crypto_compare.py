import requests
import json
import xml.etree.ElementTree as ET

# Get Bitcoin Price
def get_btc():
    cryptocompare_url = (
        'https://min-api.cryptocompare.com/data/price'
        '?fsym=BTC&tsyms=USD'
    )

    try:
        response = requests.get(cryptocompare_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'USD' in data:
            return float(data['USD'])
    except (requests.RequestException, ValueError):
        pass

    coingecko_url = (
        'https://api.coingecko.com/api/v3/simple/price'
        '?ids=bitcoin&vs_currencies=usd'
    )
    response = requests.get(coingecko_url, timeout=10)
    response.raise_for_status()
    data = response.json()

    try:
        return float(data['bitcoin']['usd'])
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError(
            'No BTC/USD price was returned by either provider.'
        ) from error

# Get BTC Full Data
def symbol(current_price=None):
    history_response = requests.get(
        'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
        '?vs_currency=usd&days=2&interval=hourly',
        timeout=10,
    )
    prices = []
    if history_response.ok:
        prices = history_response.json().get('prices', [])

    if prices:
        recent_prices = [
            price for timestamp, price in prices
            if timestamp >= prices[-1][0] - 86400000
        ]
        current_price = recent_prices[-1]
        high_day = f'${max(recent_prices):,.2f}'
        low_day = f'${min(recent_prices):,.2f}'
    else:
        current_response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price'
            '?ids=bitcoin&vs_currencies=usd',
            timeout=10,
        )
        if current_price is None and current_response.ok:
            current_price = current_response.json().get('bitcoin', {}).get('usd')
        if current_price is None:
            raise RuntimeError('BTC market data is unavailable.')
        high_day = 'Unavailable'
        low_day = 'Unavailable'

    return {
        'DISPLAY': {
            'BTC': {
                'USD': {
                    'FROMSYMBOL': 'BTC',
                    'PRICE': f'${current_price:,.2f}',
                    'HIGHDAY': high_day,
                    'LOWDAY': low_day,
                }
            }
        }
    }

# Get News Feed
def news():
    try:
        news_request = requests.get(
            'https://min-api.cryptocompare.com/data/v2/news/?lang=EN',
            timeout=10,
        )
        news_request.raise_for_status()
        payload = news_request.json()
        if payload.get('Data'):
            return payload
    except (requests.RequestException, ValueError):
        pass

    rss_request = requests.get(
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
        timeout=10,
    )
    rss_request.raise_for_status()
    root = ET.fromstring(rss_request.content)
    articles = []

    for item in root.findall('./channel/item'):
        articles.append({
            'title': item.findtext('title', default='Crypto news'),
            'url': item.findtext('link', default=''),
            'source': 'CoinDesk',
            'imageurl': '',
        })

    return {'Data': articles}

# Get Multiple Currency Full Data
def mc_symbol():
    multi_quote = 'BTC,ETH,BCH,ETC,XRP,BSV,EOS,LTC,TRX,OKB,BNB,DASH'
    mc_request = requests.get(
        'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + multi_quote + '&tsyms=USD')
    mc_symbol = json.loads(mc_request.content)
    return mc_symbol

