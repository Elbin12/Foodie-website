# Generated by Django 5.0 on 2024-01-11 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_cart_item_is_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]