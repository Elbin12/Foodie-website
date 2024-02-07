# Generated by Django 5.0 on 2023-12-30 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_cart_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_items',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='accounts.cart'),
        ),
    ]
