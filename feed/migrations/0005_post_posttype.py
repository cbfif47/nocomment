# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20170227_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='postType',
            field=models.TextField(default='Video'),
        ),
    ]