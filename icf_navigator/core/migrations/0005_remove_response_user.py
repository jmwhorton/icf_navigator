# Generated by Django 3.1.2 on 2020-10-05 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201004_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='user',
        ),
    ]