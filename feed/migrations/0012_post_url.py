# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 18:38
from __future__ import unicode_literals

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_auto_20170228_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=embed_video.fields.EmbedVideoField(default='https://www.youtube.com/watch?v=tfWgs3xXBVM'),
            preserve_default=False,
        ),
    ]
