# Generated by Django 5.0 on 2024-01-27 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_rename_extra_price_productattribute_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='price',
        ),
    ]
