# Generated by Django 5.0 on 2023-12-29 18:08

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_starts_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='starts_from',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Sub_category',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('sub_category_name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='products.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
