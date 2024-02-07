# Generated by Django 5.0 on 2024-01-28 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_alter_my_coupon_valid_till'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mob',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='my_coupon',
            name='valid_till',
            field=models.DateField(default=datetime.datetime(2024, 2, 27, 7, 6, 31, 868683)),
        ),
    ]