# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0008_auto_20150303_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='photo_big_thumb',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
