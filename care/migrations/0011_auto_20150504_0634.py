# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0010_auto_20150304_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='donator',
            field=models.CharField(max_length=50, verbose_name='UID \u0431\u043b\u0430\u0433\u043e\u0434\u0456\u0439\u043d\u0438\u043a\u0430'),
        ),
        migrations.AlterField(
            model_name='tagtranslation',
            name='name',
            field=models.CharField(max_length=75, verbose_name='\u0422\u0435\u0433'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='original_picture',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f \u0444\u0430\u0439\u043b\u0443', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_picture',
            field=models.CharField(default=b'', max_length=255, verbose_name='URL \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0456\u0457', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_thumbnail',
            field=models.CharField(default=b'', max_length=255, verbose_name='URL \u043e\u0431\u043a\u043b\u0430\u0434\u0438\u043d\u043a\u0438', blank=True),
        ),
    ]
