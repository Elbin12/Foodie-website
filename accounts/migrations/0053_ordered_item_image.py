# Generated by Django 5.0 on 2024-01-29 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_order_coupon_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordered_item',
            name='image',
            field=models.ImageField(null=True, upload_to='ordered_item'),
        ),
    ]