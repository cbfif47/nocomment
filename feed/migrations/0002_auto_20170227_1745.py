# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name',
            field=models.TextField(default='New Post'),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.TextField(default='New Source'),
        ),
    ]
