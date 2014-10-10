# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0006_auto_20141005_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='category',
            field=models.ManyToManyField(to=b'care.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='date_approve',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='date_pub',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='tag',
            field=models.ManyToManyField(to=b'care.Tag', blank=True),
        ),
    ]
