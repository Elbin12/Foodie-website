# Generated by Django 5.0 on 2024-02-20 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0073_ordered_item_product_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordered_item',
            name='ordered_product_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]