# Generated by Django 5.0 on 2024-01-27 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_alter_my_coupon_valid_till'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_coupon',
            name='valid_till',
            field=models.DateField(default=datetime.datetime(2024, 2, 26, 11, 55, 16, 405824)),
        ),
    ]
