# Generated by Django 5.0 on 2024-01-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_address_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='locality',
            field=models.CharField(blank=True, null=True),
        ),
    ]
