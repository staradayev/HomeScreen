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

		

class Picture(MultilingualModel):

	"""
	three size sets:
		thumbnail (photo_thumb)
		medium (photo_medium)
		original (photo_FULL_HD)
	"""
	def path_and_rename(path):
		def wrapper(instance, filename):
			now = str(int(time.time()))
			hashPath = hashlib.md5(now).hexdigest()
			path = 'gallery/'+hashPath[:2]+'/'+hashPath[2:4]+'/'+hashPath+'/'
			ext = filename.split('.')[-1]
			# get filename
			filename = '{}.{}'.format(uuid4().hex, ext)
			# return the whole path to the file
			return os.path.join(path, filename)
		return wrapper

	
	#picture_name = models.CharField(verbose_name=_(u"Picture name"), maxength=100)
	date_pub = models.DateTimeField(auto_now_add=True, auto_now=True)
	approve_status = models.BooleanField(default=False)
	date_approve = models.DateTimeField(null=True)
	photo_origin = models.ImageField(verbose_name=_(u"original file upload"), upload_to=path_and_rename('gallerydef/'))
	photo_medium = models.CharField(max_length=255, blank=True)
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
		sizes = {'thumbnail': {'height': 240, 'width': 320}, 'medium': {'height': 480, 'width': 640}, 'fullHD': {'height': 1080, 'width': 1920},}

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

			# create thumbnail (sqare - no need lands or port)
			im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
			#thumbname = filename + "_" + str(sizes['thumbnail']['width']) + "x" + str(sizes['thumbnail']['height']) + ".jpg"
			thumbname = uuid4().hex + ".jpg"
			im.save(fullpath + '/' + thumbname)
			#add_watermark(fullpath + '/' + thumbname, "ATO.care", fullpath + '/' + thumbname)
			self.photo_thumb = filepath + thumbname

			super(Picture, self).save()
			add_watermark(fullpath + '/' + medname, "ATO.care", fullpath + '/' + medname)

FONT = 'ARIAL.TTF'

def add_watermark(in_file, text, out_file='watermark.jpg', angle=23, opacity=0.25):
	print in_file
	img = Image.open(in_file).convert('RGB')
	watermark = Image.new('RGBA', img.size, (0,0,0,0))
	size = 2
	print settings.STATIC_ROOT + "css/" + FONT
	n_font = ImageFont.truetype(settings.STATIC_ROOT + "css/" + FONT, size)
	n_width, n_height = n_font.getsize(text)
	while n_width+n_height < watermark.size[0]:
		size += 2
		n_font = ImageFont.truetype(settings.STATIC_ROOT + "css/" + FONT, size)
		n_width, n_height = n_font.getsize(text)
	draw = ImageDraw.Draw(watermark, 'RGBA')
	draw.text(((watermark.size[0] - n_width) / 2,
			  (watermark.size[1] - n_height) / 2),
			  text, font=n_font)
	watermark = watermark.rotate(angle,Image.BICUBIC)
	alpha = watermark.split()[3]
	alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
	watermark.putalpha(alpha)
	Image.composite(watermark, img, watermark).save(out_file, 'JPEG')

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

	@classmethod
	def create(cls, user):
		up = cls(user=user)
		# do something with the book
		return up
	user = models.ForeignKey(User, unique=True)
	links = models.ManyToManyField(Link, blank=True)

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
	organization = models.ForeignKey(Organization)
	donator = models.CharField(verbose_name=_(u"Donator uiid"), max_length=50)
	t_uuid = models.CharField(verbose_name=_(u"Transaction uiid"), max_length=400)

class Like(models.Model):
	picture = models.ForeignKey(Picture, unique=True)
	user = models.CharField('user uiid', max_length=50)
	date_pub = models.DateTimeField(auto_now_add=True)
		






	
