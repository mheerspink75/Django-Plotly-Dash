from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usd_balance = models.DecimalField(max_digits=12, decimal_places=2, default=100000)
    bitcoin_balance = models.DecimalField(max_digits=12, decimal_places=2, default=1)


