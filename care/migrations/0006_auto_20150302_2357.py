# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0005_auto_20150302_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='image',
            new_name='photo',
        ),
    ]
