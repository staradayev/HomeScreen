# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0009_picture_photo_big_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='original_picture',
            field=models.CharField(default=b'', max_length=255, verbose_name='original_url', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_thumbnail',
            field=models.CharField(default=b'', max_length=255, verbose_name='thumbnail_url', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_picture',
            field=models.CharField(default=b'', max_length=255, verbose_name='photo_url', blank=True),
        ),
    ]
