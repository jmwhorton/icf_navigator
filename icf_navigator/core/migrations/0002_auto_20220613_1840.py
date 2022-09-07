# Generated by Django 3.1.14 on 2022-06-13 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='canned_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='canned_no', to='core.cannedtext'),
        ),
        migrations.AddField(
            model_name='question',
            name='canned_yes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='canned_yes', to='core.cannedtext'),
        ),
        migrations.AddField(
            model_name='qgroup',
            name='questions',
            field=models.ManyToManyField(blank=True, to='core.Question'),
        ),
        migrations.AddField(
            model_name='qgroup',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.section'),
        ),
        migrations.AddField(
            model_name='edittext',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.response'),
        ),
        migrations.AddField(
            model_name='consentform',
            name='authorized_users',
            field=models.ManyToManyField(to='users.PotentialUser'),
        ),
        migrations.CreateModel(
            name='ContactQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='CustomQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='FreeTextQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='IntegerQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='MultiSelectQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='TextListQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='YesNoExplainQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.CreateModel(
            name='YesNoQuestion',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.question',),
        ),
        migrations.AlterUniqueTogether(
            name='response',
            unique_together={('form', 'question')},
        ),
        migrations.AlterUniqueTogether(
            name='qgroup',
            unique_together={('order', 'section')},
        ),
    ]