# Generated by Django 5.0 on 2024-01-18 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_attributes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]
