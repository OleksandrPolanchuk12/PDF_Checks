# Generated by Django 5.1.6 on 2025-03-25 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0002_alter_printer_point_id'),
        ('rest_framework_api_key', '0005_auto_20220110_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printer',
            name='api_key',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rest_framework_api_key.apikey'),
        ),
    ]
