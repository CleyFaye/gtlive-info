# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0008_auto_20180305_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(help_text='The name of the game or activity performed on the stream', max_length=200, unique=True, verbose_name='Name of the game/activity'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='scheduled_date',
            field=models.DateTimeField(blank=True, help_text='The expected streaming date, or if changed afterward, the actual streaming date.', null=True, unique=True, verbose_name='Scheduled streaming date and time'),
        ),
    ]
