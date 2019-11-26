[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io#snapshot/87f30c6c-4307-46d1-abca-1425bcf8d5b3)

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
from app1.models import Account

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

User.objects.get(id=1).account.user.username





```