# Generated by Django 5.0 on 2024-01-04 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_category',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]