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

```
py manage.py shell

>>> from django.contrib.auth.models import User
>>> User._meta.get_field('username')
>>> User._meta.get_fields()
# Also include hidden fields.
>>> User._meta.get_fields(include_hidden=True)

And to store numbers up to approximately one billion with a resolution of 10 decimal places:

models.DecimalField(..., max_digits=19, decimal_places=10)

>>> print(User._meta.get_fields())
(<ManyToOneRel: admin.logentry>, <django.db.models.fields.AutoField: id>, <django.db.models.fields.CharField: password>, <django.db.models.fields.DateTimeField: last_login>, <django.db.models.fields.BooleanField: is_superuser>, <django.db.models.fields.CharField: username>, <django.db.models.fields.CharField: first_name>, <django.db.models.fields.CharField: last_name>, <django.db.models.fields.EmailField: email>, <django.db.models.fields.BooleanField: is_staff>, <django.db.models.fields.BooleanField: is_active>, <django.db.models.fields.DateTimeField: date_joined>, <django.db.models.fields.related.ManyToManyField: groups>, <django.db.models.fields.related.ManyToManyField: user_permissions>)


```
DecimalField
The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

DateTimeField
class DateTimeField(auto_now=False, auto_now_add=False, **options)[source]¶
A date and time, represented in Python by a datetime.datetime instance. Takes the same extra arguments as DateField.

The default form widget for this field is a single TextInput. The admin uses two separate TextInput widgets with JavaScript shortcuts.