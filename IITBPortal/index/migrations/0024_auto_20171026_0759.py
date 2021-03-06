# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_auto_20171026_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='news_feed',
            name='my_tag',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='course',
            name='all_students',
            field=models.ManyToManyField(default=None, to='index.Student'),
        ),
        migrations.AlterField(
            model_name='interest',
            name='all_students',
            field=models.ManyToManyField(to='index.Student'),
        ),
    ]
