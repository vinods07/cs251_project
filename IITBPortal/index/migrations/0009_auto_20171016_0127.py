# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-10-16 01:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20171016_0118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='course',
            new_name='std',
        ),
    ]