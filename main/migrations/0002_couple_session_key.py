# Generated by Django 3.1.7 on 2021-03-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='couple',
            name='session_key',
            field=models.CharField(default=None, max_length=256, verbose_name='Идентификатор сессии'),
        ),
    ]
