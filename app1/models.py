from django.db import models
from django.contrib.auth.models import User
import requests


TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
def get_latest_crypto_price( crypto ):
    response = requests.get(TICKER_API_URL+crypto)
    response_json = response.json()
    return float(response_json[0]['price_usd'])

BTC_PRICE = get_latest_crypto_price('bitcoin')

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    usd_balance = models.DecimalField(max_digits=12, decimal_places=2, default=100000)
    bitcoin_balance = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    bitcoin_price = models.DecimalField(max_digits=12, decimal_places=2, default=BTC_PRICE)


