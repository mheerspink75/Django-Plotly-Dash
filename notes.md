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

requirements.txt

autopep8==1.4.4
certifi==2019.9.11
chardet==3.0.4
Click==7.0
dash==1.6.1
dash-core-components==1.5.1
dash-html-components==1.0.2
dash-renderer==1.2.1
dash-table==4.5.1
dj-database-url==0.5.0
Django==2.2.7
django-crispy-forms==1.8.0
django-plotly-dash==1.0.2
dpd-components==0.1.0
Flask==1.1.1
Flask-Compress==1.4.0
future==0.18.2
gunicorn==20.0.0
idna==2.8
itsdangerous==1.1.0
Jinja2==2.10.3
lxml==4.4.1
MarkupSafe==1.1.1
numpy==1.17.4
pandas==0.25.3
pandas-datareader==0.8.1
plotly==4.3.0
psycopg2==2.8.4
pycodestyle==2.5.0
python-dateutil==2.8.1
pytz==2019.3
requests==2.22.0
retrying==1.3.3
six==1.13.0
sqlparse==0.3.0
urllib3==1.25.7
Werkzeug==0.16.0
whitenoise==4.1.4

pip install pur
pur -r requirements.txt

Updated autopep8: 1.4.4 -> 1.5
Updated certifi: 2019.9.11 -> 2019.11.28
Updated dash: 1.6.1 -> 1.8.0
Updated dash-core-components: 1.5.1 -> 1.7.0
Updated dash-renderer: 1.2.1 -> 1.2.3
Updated dash-table: 4.5.1 -> 4.6.0
Updated Django: 2.2.7 -> 3.0.2
Updated django-crispy-forms: 1.8.0 -> 1.8.1
Updated django-plotly-dash: 1.0.2 -> 1.1.5
Updated gunicorn: 20.0.0 -> 20.0.4
Updated lxml: 4.4.1 -> 4.4.2
Updated numpy: 1.17.4 -> 1.18.1
Updated plotly: 4.3.0 -> 4.5.0
Updated six: 1.13.0 -> 1.14.0
Updated urllib3: 1.25.7 -> 1.25.8
Updated whitenoise: 4.1.4 -> 5.0.1
All requirements up-to-date.