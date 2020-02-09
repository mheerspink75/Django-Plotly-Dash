# Generated by Django 3.0.2 on 2020-02-08 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usd_balance', models.DecimalField(decimal_places=2, default=50000, max_digits=12)),
                ('bitcoin_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('transaction_type', models.CharField(max_length=5)),
                ('transaction_date', models.DateTimeField()),
                ('transaction_btc_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('transaction_usd_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
