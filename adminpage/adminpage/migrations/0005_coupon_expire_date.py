# Generated by Django 5.0 on 2024-01-29 04:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0004_alter_coupon_no_of_coupons'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='expire_date',
            field=models.DateTimeField(default=datetime.date(2024, 2, 28)),
        ),
    ]