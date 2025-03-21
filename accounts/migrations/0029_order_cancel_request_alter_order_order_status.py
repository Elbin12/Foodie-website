# Generated by Django 5.0 on 2024-01-22 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_ordered_item_price_alter_ordered_item_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancel_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Cancelled by admin', 'Cancelled by admin')], default='Pending', max_length=20),
        ),
    ]
