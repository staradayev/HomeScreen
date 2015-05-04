# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0011_auto_20150504_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='donator',
            field=models.CharField(max_length=50, verbose_name='UID \u0436\u0435\u0440\u0442\u0432\u043e\u0434\u0430\u0432\u0446\u044f'),
        ),
    ]
