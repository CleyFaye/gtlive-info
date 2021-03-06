# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-06 16:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_date', models.DateTimeField(blank=True, help_text='Date at which the article will become visible', null=True, verbose_name='Publication date')),
                ('expiration_date', models.DateTimeField(blank=True, help_text='Date at which the article will become invisible. Can be left blank if the article should not expire.', null=True, verbose_name='Expiration date')),
                ('title', models.CharField(help_text='The full title, displayed in lists and before content', max_length=500, verbose_name='Title')),
                ('content', models.TextField(help_text="The article's content. Support markdown.", verbose_name='Content')),
            ],
            options={
                'ordering': ('publication_date',),
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Visible author name', max_length=200, unique=True, verbose_name='Author name')),
                ('twitter', models.CharField(blank=True, help_text='Twitter handle for this author identity', max_length=30, null=True, verbose_name='Twitter handle')),
                ('user', models.ManyToManyField(help_text='List of users that can use this identity to publish articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(help_text='The identity under which the article is published', on_delete=django.db.models.deletion.CASCADE, to='blog.Author'),
        ),
    ]
