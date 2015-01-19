# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0002_picture_complete_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='tag',
            field=models.ManyToManyField(to='care.Tag', blank=True),
            preserve_default=True,
        ),
    ]
