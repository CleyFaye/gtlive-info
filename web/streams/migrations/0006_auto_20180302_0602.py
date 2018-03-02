# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-02 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0005_auto_20180302_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='archive_thumbnail',
            field=models.ImageField(blank=True, help_text='The thumbnail used on the archive video', null=True, upload_to='', verbose_name='Thumbnail of the archive video'),
        ),
        migrations.AddField(
            model_name='stream',
            name='live_thumbnail',
            field=models.ImageField(blank=True, help_text='The thumbnail used on the full stream, on the main channel', null=True, upload_to='', verbose_name='Thumbnail of the full video'),
        ),
    ]