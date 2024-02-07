# Generated by Django 5.0 on 2024-01-28 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0050_my_coupon'),
        ('adminpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='applied_coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applied_coupon', to='adminpage.coupon'),
        ),
        migrations.DeleteModel(
            name='My_coupon',
        ),
    ]
