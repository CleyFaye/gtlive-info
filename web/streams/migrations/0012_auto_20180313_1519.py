# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-13 22:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0011_auto_20180313_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='archive_thumbnail',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='archive_title',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='archive_yt_ref',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='live_thumbnail',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='live_title',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='live_yt_ref',
        ),
    ]
