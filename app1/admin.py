from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_balance', 'account_date', 'cash_balance', 'transaction_date', 'transaction_type', 'transaction_amount')

admin.site.register(Account, AccountAdmin)

