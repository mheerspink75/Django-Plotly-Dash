from django.contrib import admin
from .models import Account, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'usd_balance', 'bitcoin_balance')

admin.site.register(Account, AccountAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'transaction_date', 'transaction_btc', 'transaction_usd')

admin.site.register(Transaction, TransactionAdmin)


