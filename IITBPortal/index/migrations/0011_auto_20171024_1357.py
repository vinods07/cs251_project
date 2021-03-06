# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 13:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('index', '0010_auto_20171024_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(default='', max_length=250)),
                ('assignment_content_file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(default='', max_length=20)),
                ('course_name', models.CharField(default='', max_length=250)),
                ('course_info', models.CharField(default='', max_length=500)),
                ('all_students', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_material_name', models.CharField(max_length=250)),
                ('course_material_info', models.TextField()),
                ('course_content_file', models.FileField(blank=True, null=True, upload_to='')),
                ('parent_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Course')),
            ],
        ),
        migrations.RemoveField(
            model_name='courses',
            name='all_students',
        ),
        migrations.RemoveField(
            model_name='courses',
            name='std',
        ),
        migrations.DeleteModel(
            name='courses',
        ),
        migrations.AddField(
            model_name='assignment',
            name='parent_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='submissions',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
