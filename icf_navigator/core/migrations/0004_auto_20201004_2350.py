# Generated by Django 3.1.2 on 2020-10-04 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201004_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.FloatField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]