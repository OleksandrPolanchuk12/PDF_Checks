# Generated by Django 5.1.6 on 2025-02-21 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0002_check_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='number',
        ),
    ]
