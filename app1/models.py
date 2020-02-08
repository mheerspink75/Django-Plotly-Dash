from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usd_balance = models.DecimalField(max_digits=12, decimal_places=2, default=50000)
    bitcoin_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=5)
    transaction_date = models.DateTimeField()
    transaction_btc = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transaction_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)



@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()

