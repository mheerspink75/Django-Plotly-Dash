from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usd_balance = models.DecimalField(max_digits=12, decimal_places=2, default=100000)
    bitcoin_balance = models.DecimalField(max_digits=12, decimal_places=2, default=2)

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()
