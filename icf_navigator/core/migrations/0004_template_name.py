# Generated by Django 3.1.14 on 2022-08-04 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='name',
            field=models.CharField(default='home.html', max_length=100),
            preserve_default=False,
        ),
    ]