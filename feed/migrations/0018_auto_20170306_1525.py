# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 23:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0017_auto_20170306_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='postType',
            new_name='post_type',
        ),
        migrations.RenameField(
            model_name='rawpost',
            old_name='postType',
            new_name='post_type',
        ),
        migrations.RenameField(
            model_name='scoredpost',
            old_name='postType',
            new_name='post_type',
        ),
    ]
