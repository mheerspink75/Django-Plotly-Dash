https://pypi.org/project/django-plotly-dash/

https://django-plotly-dash.readthedocs.io/en/latest/introduction.html

https://dash.plot.ly/

https://docs.djangoproject.com/en/2.2/ref/templates/language/#template-inheritance

https://www.youtube.com/playlist?list=PLsyeobzWxl7r2ukVgTqIQcl-1T0C2mzau

https://docs.djangoproject.com/en/2.2/topics/db/models/#


heroku git:remote -a django-machtrade

heroku: https://django-machtrade.herokuapp.com/

https://ultimatedjango.com/learn-django/lessons/push-to-heroku/

---

### Add user login

https://www.youtube.com/watch?v=Ev5xgwndmfc

https://www.youtube.com/watch?v=z4lfVsb_7MA&t=420s

https://pythonprogramming.net/user-login-logout-django-tutorial/

### Custom user models

https://www.youtube.com/watch?v=sXZ3ntGp_Xc

https://www.youtube.com/watch?v=Fy02hU7eFtg

https://www.youtube.com/watch?v=HshbjK1vDtY

https://docs.djangoproject.com/en/2.2/ref/models/fields/#

https://docs.djangoproject.com/en/2.2/topics/auth/customizing/

https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

http://www.learningaboutelectronics.com/Articles/How-to-add-a-price-field-to-a-database-table-in-Django.php

https://books.agiliq.com/projects/django-admin-cookbook/en/latest/change_text.html

https://books.agiliq.com/projects/django-orm-cookbook/en/latest/


### Add user account transactions
```
py manage.py shell

>>> from django.contrib.auth.models import User
>>> User._meta.get_field('username')
>>> User._meta.get_fields()
# Also include hidden fields.
>>> User._meta.get_fields(include_hidden=True)
```
>>> print(User._meta.get_fields())
(<ManyToOneRel: admin.logentry>, <django.db.models.fields.AutoField: id>, <django.db.models.fields.CharField: password>, <django.db.models.fields.DateTimeField: last_login>, <django.db.models.fields.BooleanField: is_superuser>, <django.db.models.fields.CharField: username>, <django.db.models.fields.CharField: first_name>, <django.db.models.fields.CharField: last_name>, <django.db.models.fields.EmailField: email>, <django.db.models.fields.BooleanField: is_staff>, <django.db.models.fields.BooleanField: is_active>, <django.db.models.fields.DateTimeField: date_joined>, <django.db.models.fields.related.ManyToManyField: groups>, <django.db.models.fields.related.ManyToManyField: user_permissions>)

And to store numbers up to approximately one billion with a resolution of 10 decimal places:

models.DecimalField(..., max_digits=19, decimal_places=10)
DecimalField
The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

DateTimeField
class DateTimeField(auto_now=False, auto_now_add=False, **options)[source]¶
A date and time, represented in Python by a datetime.datetime instance. Takes the same extra arguments as DateField.

The default form widget for this field is a single TextInput. The admin uses two separate TextInput widgets with JavaScript shortcuts.

>>> from django.contrib.auth.models import User
>>> User._meta.get_fields(include_hidden=True)
(<ManyToOneRel: admin.logentry>, <ManyToOneRel: auth.user_groups>, <ManyToOneRel: auth.user_user_permissions>, <OneToOneRel: app1.account>, <django.db.models.fields.AutoField: id>, <django.db.models.fields.CharField: password>, <django.db.models.fields.DateTimeField: last_login>, <django.db.models.fields.BooleanField: is_superuser>, <django.db.models.fields.CharField: username>, <django.db.models.fields.CharField: first_name>, <django.db.models.fields.CharField: last_name>, <django.db.models.fields.EmailField: email>, <django.db.models.fields.BooleanField: is_staff>, <django.db.models.fields.BooleanField: is_active>, <django.db.models.fields.DateTimeField: date_joined>, <django.db.models.fields.related.ManyToManyField: groups>, <django.db.models.fields.related.ManyToManyField: user_permissions>)

>>> User._meta.get_field('account')

{{ user.account.account_balance }}

### Python to db
```
py manage.py shell

from django.contrib.auth.models import User
from django.db import models
from app1.models import Account, Transactions

from app1.models import Transactions
.

User.objects.all()
<QuerySet [<User: mattheerspink>, <User: mh1975>, <User: user5000>]>

Account.objects.all()
<QuerySet [<Account: Account object (1)>, <Account: Account object (2)>, <Account: Account object (3)>]>

Account1 = Account.objects.first()
Account1_user = Account1.user

>>> Account1
<Account: Account object (1)>

>>> Account1_user
<User: mh1975>

>>> Account1_user.username
'mh1975'

Account.objects.first().user.username

Account.objects.all()
Account.objects.get(id=1).user.username

Account.objects.get(id=1).account_balance
Account.objects.get(id=3).cash_balance    

Account.objects.get(id=1)

account = Account.objects.all()
str(account.query)


str(User.objects.all().query)

str(Account.objects.all().query)

User.objects.get(pk=1).account.user.username

Account.objects.count()

Account.objects.values()

User.objects.get(id=1).username


Transactions.objects.all()
Transactions.objects.all().filter(user=Account.user.username)


```
Django Forms: 
https://www.youtube.com/playlist?list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO
https://www.youtube.com/watch?v=EX6Tt-ZW0so

https://www.youtube.com/watch?v=uu98pqiUJU8&list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW


Need to do:

1. Allocate each user an account cash balance automatically when the user is created. X
   
2. Create a django form that pulls the current BTC/USD price from an API request, allows the user to buy and sell BTC/USD, calculates the transaction amounts, updates the form with the BTC/USD quantities and tracks the portfolio value in USD. X

3. The form needs to post to the database when transactions are completed. X

4. The form needs to post transaction amounts, order type (buy/sell) and post transaction history to the database. X

5. Need to calculate portfolio value from the database  X and visiualize the data with a chart. X

6. Models needs a transaction class for buys and sells. X

7. Foriegn Key goes in the account class that points at the transaction similar to the blog post tutorial. X


-------------------------
1. build models and views to log transactions, The form needs to post transaction amounts, order type (buy/sell) and post transaction history to the database. X

2. Visiualize user portfolio daily balance history. X

3. Work on styling the site. X

4. Add buy and sell user interface. X

5. Add chart update search results to symbol lookup. X

6. Add and account history page and account reset. X

https://www.geeksforgeeks.org/python-relational-fields-in-django-models/

https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model




=> Duplicate the workspace.

Open the command pannel ctrl+shift+p or F1. Then write dupl


from django.contrib.auth.models import User
from django.db import models
from app1.models import Account, Transactions
from app1.models import Transactions

Transactions.objects.all()
Transactions.objects.all().order_by('transaction_date')
Transactions.objects.all().get(user='mattheerspink')
Transactions.objects.get(id=1).id
Transactions.objects.filter(user_id=1).values_list('id', flat=True)
Transactions.objects.filter(user_id=1).values_list('id', flat=True).reverse()
Transactions.objects.filter(user_id=1).reverse().values_list('id', flat=True)
reversed(Transactions.objects.all().order_by('transaction_date').filter(user_id=1))

Transactions.objects.create(transaction_date=timezone.datetime.now())
Transactions.objects.create(user_id=1, transaction_date=timezone.datetime.now())




