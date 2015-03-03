# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0007_auto_20150302_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='picture',
        ),
        migrations.AddField(
            model_name='like',
            name='photo',
            field=models.ForeignKey(default=7, to='care.Picture'),
            preserve_default=False,
        ),
    ]
