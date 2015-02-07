# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0003_download_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytranslation',
            name='language_code',
            field=models.CharField(max_length=7, verbose_name='language', choices=[(b'ua', b'Ukrainian'), (b'en', b'English')]),
        ),
        migrations.AlterField(
            model_name='organizationtranslation',
            name='language_code',
            field=models.CharField(max_length=7, verbose_name='language', choices=[(b'ua', b'Ukrainian'), (b'en', b'English')]),
        ),
        migrations.AlterField(
            model_name='picturetranslation',
            name='language_code',
            field=models.CharField(max_length=7, verbose_name='language', choices=[(b'ua', b'Ukrainian'), (b'en', b'English')]),
        ),
        migrations.AlterField(
            model_name='tagtranslation',
            name='language_code',
            field=models.CharField(max_length=7, verbose_name='language', choices=[(b'ua', b'Ukrainian'), (b'en', b'English')]),
        ),
    ]
