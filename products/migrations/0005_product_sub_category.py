# Generated by Django 5.0 on 2023-12-29 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_starts_from_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='products.sub_category'),
        ),
    ]
