# Generated by Django 5.0 on 2024-01-23 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_profile_first_name_profile_gender_profile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_image',
        ),
    ]