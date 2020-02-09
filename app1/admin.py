from django.contrib import admin
from .models import Account, Transactions

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'usd_balance', 'bitcoin_balance', 'transaction_type', 'transaction_date', 'transaction_btc_quantity', 'transaction_usd_price', 'transaction_total_usd_price')

admin.site.register(Account, AccountAdmin)

admin.site.register(Transactions)



'''
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'transaction_date', 'transaction_btc', 'transaction_usd')

admin.site.register(Transaction, TransactionAdmin)
'''

