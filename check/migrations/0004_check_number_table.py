# Generated by Django 5.1.6 on 2025-03-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0003_remove_check_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='number_table',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
