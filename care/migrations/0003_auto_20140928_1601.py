# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0002_category_picture_tag'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='picture',
            name='category',
            field=models.ManyToManyField(to='care.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='picture',
            name='tag',
            field=models.ManyToManyField(to='care.Tag'),
            preserve_default=True,
        ),
    ]
