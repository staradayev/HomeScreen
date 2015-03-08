from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys, time
import hashlib
from uuid import uuid4
import os
from django import forms
from multilingual_model.models import MultilingualModel, MultilingualTranslation
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.conf import settings
import helpers
from django.utils.deconstruct import deconstructible
from django.db.models.signals import pre_delete


class Tag(MultilingualModel):
    #tag_name = models.CharField(verbose_name=_(u"#tagname"), max_length=50)
    date_pub = models.DateTimeField(auto_now_add=True)
    approve_status = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    def __str__(self):
        try:
            return self.translations.get(pk=self.id).name.encode('utf-8') or _(u'Unnamed')
        except TagTranslation.DoesNotExist:
            return _(u'Unnamed')
    @classmethod
    def create(cls, author):
        tag_obj = cls(author=author)
        # do something with the picture
        return tag_obj


class TagTranslation(MultilingualTranslation):
    class Meta:
        unique_together = ('parent', 'language_code')

    parent = models.ForeignKey(Tag, related_name='translations')
    name = models.CharField(verbose_name=_(u"#tagname"), max_length=75)


class Category(MultilingualModel):
    def download_count(self):
        return self.download_set.filter().count()

    date_pub = models.DateTimeField(auto_now_add=True)
    approve_status = models.BooleanField(default=False)
    author = models.ForeignKey(User)

    def __str__(self):
        try:
            return self.translations.get(pk=self.id).name.encode('utf-8') or _(u'Unnamed')
        except CategoryTranslation.DoesNotExist:
            return _(u'Unnamed')
    @classmethod
    def create(cls, author):
        cat_obj = cls(author=author)
        # do something with the picture
        return cat_obj


class CategoryTranslation(MultilingualTranslation):
    class Meta:
        unique_together = ('parent', 'language_code')

    parent = models.ForeignKey(Category, related_name='translations')
    name = models.CharField(verbose_name=_(u"Category name"), max_length=75)

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        now = str(int(time.time()))
        hashPath = hashlib.md5(now).hexdigest()
        path = 'gallery/'+hashPath[:2]+'/'+hashPath[2:4]+'/'+hashPath+'/'
        ext = filename.split('.')[-1]
        # get filename
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)

class Picture(MultilingualModel):

    """
    four size sets:
        thumbnail (photo_big_thumb)
        bigthumbnail (photo_thumb)
        medium (photo_medium)
        original (photo_FULL_HD)
    """

    path_and_rename = PathAndRename('gallerydef/')


    #picture_name = models.CharField(verbose_name=_(u"Picture name"), maxength=100)
    date_pub = models.DateTimeField(auto_now_add=True, auto_now=True)
    approve_status = models.BooleanField(default=False)
    complete_status = models.BooleanField(default=False)
    date_approve = models.DateTimeField(null=True)
    photo_origin = models.ImageField(verbose_name=_(u"original file upload"), upload_to=path_and_rename)
    photo_medium = models.CharField(max_length=255, blank=True)
    photo_big_thumb = models.CharField(max_length=255, blank=True, default='')
    photo_thumb = models.CharField(max_length=255, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)

    def download_count(self):
        return self.download_set.filter().count()

    def __str__(self):
        try:
            return self.translations.get(pk=self.id).name.encode('utf-8') or _(u'Unnamed')
        except PictureTranslation.DoesNotExist:
            return _(u'Unnamed')

    def get_thumb(self):
        return "/media/%s" % self.photo_thumb

    def get_big_thumb(self):
        return "/media/%s" % self.photo_big_thumb

    def get_medium(self):
        return "/media/%s" % self.photo_medium

    def get_original(self):
        return "/media/%s" % self.photo_origin

    def __iter__(self):
        return self

    def admin_thumbnail(self):
        return u'<img src="/media/%s" />' % (self.photo_thumb)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    @classmethod
    def create(cls, picture, user_added):
        image_obj = cls(photo_origin=picture, author=user_added)
        # do something with the picture
        return image_obj

    def save(self):
        sizes = {'big_thumbnail': {'height': 600, 'width': 600}, 'thumbnail': {'height': 240, 'width': 320}, 'medium': {'height': 480, 'width': 640}, 'fullHD': {'height': 1080, 'width': 1920},}

        super(Picture, self).save()
        if not self.photo_medium:
            photopath = str(self.photo_origin.path)  # this returns the full system path to the original file
            print photopath
            im = Image.open(photopath)  # open the image using PIL

            # pull a few variables out of that full path
            extension = photopath.rsplit('.', 1)[1]  # the file extension
            filename = photopath.rsplit('/', 1)[1].rsplit('.', 1)[0]  # the file name only (minus path or extension)
            fullpath = photopath.rsplit('/', 1)[0]  # the path only (minus the filename.extension)

            # use the file extension to determine if the image is valid before proceeding
            if extension.lower() not in ['jpg', 'jpeg', 'gif', 'png']:
                super(Picture, self).delete()
                sys.exit()

            now = str(int(time.time()))
            hashPath = hashlib.md5(now).hexdigest()
            filepath = 'gallery/'+hashPath[:2]+'/'+hashPath[2:4]+'/'+hashPath+'/'

            (width, height) = im.size

            if(width > height):
                # create fullHD image lands
                im.thumbnail((sizes['fullHD']['width'], sizes['fullHD']['height']), Image.ANTIALIAS)
            else:
                # create fullHD image port
                im.thumbnail((sizes['fullHD']['height'], sizes['fullHD']['width']), Image.ANTIALIAS)

            fullHD = filename + ".jpg"
            im.save(fullpath + '/' + fullHD)

            if(width > height):
                # create medium image lands
                im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
            else:
                # create medium image port
                im.thumbnail((sizes['medium']['height'], sizes['medium']['width']), Image.ANTIALIAS)
            #medname = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height']) + ".jpg"
            medname = uuid4().hex + ".jpg"
            im.save(fullpath + '/' + medname)

            self.photo_medium = filepath + medname

            # create thumbnail small (sqare - no need lands or port)
            im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
            #thumbname = filename + "_" + str(sizes['thumbnail']['width']) + "x" + str(sizes['thumbnail']['height']) + ".jpg"
            thumbname = uuid4().hex + ".jpg"
            im.save(fullpath + '/' + thumbname)
            #add_watermark(fullpath + '/' + thumbname, "ATO.care", fullpath + '/' + thumbname)
            self.photo_thumb = filepath + thumbname

            # create thumbnail small (sqare - no need lands or port)
            im.thumbnail((sizes['big_thumbnail']['width'], sizes['big_thumbnail']['height']), Image.ANTIALIAS)
            big_thumbname = uuid4().hex + ".jpg"
            im.save(fullpath + '/' + big_thumbname)
            self.photo_big_thumb = filepath + big_thumbname

            super(Picture, self).save()
            #add_watermark(fullpath + '/' + medname, "ATO.care", fullpath + '/' + medname)


def file_cleanup(sender, instance, *args, **kwargs):
    '''
        Deletes the file(s) associated with a model instance. The model
        is not saved after deletion of the file(s) since this is meant
        to be used with the pre_delete signal.
    '''

    try:
        print("Delete preview "+settings.MEDIA_ROOT + instance.photo_medium)
        os.remove(settings.MEDIA_ROOT + instance.photo_medium)
        print("Delete thumbnail "+settings.MEDIA_ROOT + instance.photo_thumb)
        os.remove(settings.MEDIA_ROOT + instance.photo_thumb)
        print("Delete big thumbnail "+settings.MEDIA_ROOT + instance.photo_big_thumb)
        os.remove(settings.MEDIA_ROOT + instance.photo_big_thumb)
    except:
        print("Can't delete thumbnail and preview of !" + str(instance.pk))

pre_delete.connect(file_cleanup, sender=Picture)

class PictureTranslation(MultilingualTranslation):
    class Meta:
        unique_together = ('parent', 'language_code')

    parent = models.ForeignKey(Picture, related_name='translations')
    name = models.CharField(verbose_name=_(u"Picture name"), max_length=100)

class LinkType(models.Model):
    type_tag = models.CharField(verbose_name=_(u"Link name"), max_length=25)
    date_pub = models.DateTimeField(auto_now_add=True)

class Link(models.Model):
    link_type = models.ForeignKey(LinkType)
    link_url = models.URLField(verbose_name=_(u"Link URL"), max_length=200)
    date_pub = models.DateTimeField(auto_now_add=True)
    @classmethod
    def create(cls, l_type):
        up = cls(link_type=l_type)
        # do something with the book
        return up

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    links = models.ManyToManyField(Link, blank=True)
    original_picture = models.CharField(verbose_name=_(u"original_url"), max_length=255, blank=True, default='')
    user_picture = models.CharField(verbose_name=_(u"photo_url"), max_length=255, blank=True, default='')
    user_thumbnail = models.CharField(verbose_name=_(u"thumbnail_url"), max_length=255, blank=True, default='')
    @classmethod
    def create(cls, user):
        up = cls(user=user)
        # do something with the book
        return up
    def get_thumb(self):
        if self.user_thumbnail:
            return "/media/%s" % self.user_thumbnail
        else:
            return settings.STATIC_URL + 'img/default/ato-user.png'

    def get_user_picture(self):
        if self.user_picture:
            return "/media/%s" % self.user_picture
        else:
            return settings.STATIC_URL + 'img/default/ato-user.png'


class Organization(MultilingualModel):
    date_pub = models.DateTimeField(auto_now_add=True)
    links = models.ManyToManyField(Link, blank=True)
    def __str__(self):
        try:
            return self.translations.get(pk=self.id).name.encode('utf-8') or _(u'Unnamed')
        except OrganizationTranslation.DoesNotExist:
            return _(u'Unnamed')

class OrganizationTranslation(MultilingualTranslation):
    class Meta:
        unique_together = ('parent', 'language_code')

    parent = models.ForeignKey(Organization, related_name='translations')
    name = models.CharField(verbose_name=_(u"Organization name"), max_length=100)
    author = models.CharField(verbose_name=_(u"Organization author"), max_length=50)
    description = models.CharField(verbose_name=_(u"Organization description"), max_length=4000)
    additional = models.CharField(verbose_name=_(u"Organization additiolal"), max_length=200)

class Download(models.Model):
    @classmethod
    def create(cls, amount, picture, organization, donator, t_uuid):
        up = cls(amount=amount, picture=picture, organization=organization, donator=donator, t_uuid=t_uuid)
        # do something with the book
        return up

    date_pub = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    picture = models.ForeignKey(Picture)
    category = models.ManyToManyField(Category, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    organization = models.ForeignKey(Organization)
    donator = models.CharField(verbose_name=_(u"Donator uiid"), max_length=50)
    t_uuid = models.CharField(verbose_name=_(u"Transaction uiid"), max_length=400)

class Like(models.Model):
    @classmethod
    def create(cls, ato_user, picture):
        like = cls(user=ato_user, photo=picture)
        # do something with the book
        return like

    photo = models.ForeignKey(Picture, unique=False)
    user = models.CharField('user uiid', max_length=50)
    date_pub = models.DateTimeField(auto_now_add=True)








