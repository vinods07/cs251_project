# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-10-10 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20171010_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='fname',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='lname',
            field=models.CharField(default='', max_length=100),
        ),
    ]
