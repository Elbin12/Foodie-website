# Generated by Django 5.0 on 2024-01-28 15:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0003_alter_coupon_no_of_coupons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='no_of_coupons',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
