# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import care.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('approve_status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=7, verbose_name='language', choices=[(b'en', b'English'), (b'ua', b'Ukrainian')])),
                ('name', models.CharField(max_length=75, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457')),
                ('parent', models.ForeignKey(related_name=b'translations', to='care.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('donator', models.CharField(max_length=50, verbose_name='UID \u0436\u0435\u0440\u0442\u0432\u043e\u0434\u0430\u0432\u0446\u044f')),
                ('t_uuid', models.CharField(max_length=400, verbose_name='UID \u0442\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0456\u0457')),
                ('category', models.ManyToManyField(to='care.Category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50, verbose_name=b'user uiid')),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_url', models.URLField(verbose_name='URL')),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_tag', models.CharField(max_length=25, verbose_name='\u041bi\u043d\u043a')),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('links', models.ManyToManyField(to='care.Link', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=7, verbose_name='language', choices=[(b'en', b'English'), (b'ua', b'Ukrainian')])),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u043e\u0440\u0433\u0430\u043d\u0456\u0437\u0430\u0446\u0456\u0457')),
                ('author', models.CharField(max_length=50, verbose_name='\u0412\u0456\u0434\u043f\u043e\u0432\u0456\u0434\u0430\u043b\u044c\u043d\u0438\u0439')),
                ('description', models.CharField(max_length=4000, verbose_name='\u041e\u043f\u0438\u0441 \u0434\u0456\u044f\u043b\u044c\u043d\u043e\u0441\u0442\u0456')),
                ('additional', models.CharField(max_length=200, verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u043e')),
                ('parent', models.ForeignKey(related_name=b'translations', to='care.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_pub', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('approve_status', models.BooleanField(default=False)),
                ('date_approve', models.DateTimeField(null=True)),
                ('photo_origin', models.ImageField(upload_to=care.models.PathAndRename(b'gallerydef/'), verbose_name='\u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f \u0444\u0430\u0439\u043b\u0443')),
                ('photo_medium', models.CharField(max_length=255, blank=True)),
                ('photo_thumb', models.CharField(max_length=255, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(to='care.Category', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PictureTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=7, verbose_name='language', choices=[(b'en', b'English'), (b'ua', b'Ukrainian')])),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u043d\u044f')),
                ('parent', models.ForeignKey(related_name=b'translations', to='care.Picture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('approve_status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=7, verbose_name='language', choices=[(b'en', b'English'), (b'ua', b'Ukrainian')])),
                ('name', models.CharField(max_length=75, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u0442\u0435\u0433\u0443')),
                ('parent', models.ForeignKey(related_name=b'translations', to='care.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_picture', models.CharField(max_length=100, verbose_name='photo_url', blank=True)),
                ('links', models.ManyToManyField(to='care.Link', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tagtranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='picturetranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
        migrations.AddField(
            model_name='picture',
            name='tag',
            field=models.ManyToManyField(to='care.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='organizationtranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
        migrations.AddField(
            model_name='link',
            name='link_type',
            field=models.ForeignKey(to='care.LinkType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='picture',
            field=models.ForeignKey(to='care.Picture', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='organization',
            field=models.ForeignKey(to='care.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='picture',
            field=models.ForeignKey(to='care.Picture'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
    ]
