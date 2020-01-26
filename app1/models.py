from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    account_date =  models.DateField(null=True, blank=True)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_type = models.CharField(max_length=30)
    transaction_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Item(models.Model):
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text