# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 22:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_scoredpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepost',
            name='score',
        ),
    ]