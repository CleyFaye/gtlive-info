# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-01 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import streams.fields.trustlevelfield
import streams.fields.youtubevideoreferencefield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the game or activity performed on the stream', max_length=200, verbose_name='Name of the game/activity')),
                ('reference', models.URLField(blank=True, help_text='Online resource to get more info (game page, etc.)', verbose_name='Online reference to get more informations')),
                ('description', models.TextField(blank=True, help_text='A brief description of the game/activity for quick reference', verbose_name='Brief description')),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateTimeField(blank=True, help_text='The expected streaming date, or if changed afterward, the actual streaming date.', null=True, verbose_name='Scheduled streaming date and time')),
                ('trust_level', streams.fields.trustlevelfield.TrustLevelField(choices=[('0', 'The most reliable of all gave us this information, it can be trusted (probably)'), ('1', "We've got some serious hints, so it's probably alright"), ('2', "Hmm. At this point, it's 50/50 wishful thinking and unreliable source, place your bets…"), ('3', "Let's be honest, this is more like a placeholder and less like a reliable information at this point.")], help_text='How much can this information be trusted.', max_length=2, verbose_name='Level of confidence for this schedule')),
                ('live_title', models.TextField(blank=True, help_text='Title of the video when it was live on the Game Theorist channel.', null=True, verbose_name='Title of the stream when it ran live')),
                ('live_yt_ref', streams.fields.youtubevideoreferencefield.YoutubeVideoReferenceField(blank=True, help_text='The Youtube reference code for the live stream.', max_length=50, null=True, verbose_name='Video reference of the live stream')),
                ('archive_title', models.TextField(blank=True, help_text='Title of the video when uploaded to the GTLive channel.', null=True, verbose_name='Title of the video when uploaded to the archive channel')),
                ('archive_yt_ref', streams.fields.youtubevideoreferencefield.YoutubeVideoReferenceField(blank=True, help_text='The Youtube reference code for the archive video.', max_length=50, null=True, verbose_name='Video reference of the archive version')),
                ('games', models.ManyToManyField(help_text='(list of) game played on the stream.', to='streams.Game')),
            ],
        ),
    ]
