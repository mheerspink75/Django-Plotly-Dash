from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio_balance', 'usd_balance', 'bitcoin_balance')

admin.site.register(Account, AccountAdmin)

