# Generated by Django 5.0 on 2024-01-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_alter_ordered_item_price_alter_ordered_item_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordered_item',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ordered_item',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
