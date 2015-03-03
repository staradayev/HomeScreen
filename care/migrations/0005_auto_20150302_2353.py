# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0004_auto_20150207_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='picture',
        ),
        migrations.AddField(
            model_name='like',
            name='image',
            field=models.ManyToManyField(to='care.Picture', blank=True),
            preserve_default=True,
        ),
    ]
