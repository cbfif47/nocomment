# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 23:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0016_source_rssable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='rawpost',
            old_name='author',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='scoredpost',
            old_name='author',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='source',
            name='author',
        ),
    ]
