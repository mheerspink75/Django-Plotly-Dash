from django.contrib import admin
from .models import Account, Transactions

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'usd_balance', 'bitcoin_balance')

admin.site.register(Account, AccountAdmin)

admin.site.register(Transactions)



