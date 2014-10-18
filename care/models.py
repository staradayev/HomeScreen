from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import sys, time
import hashlib
from uuid import uuid4
import os
from django import forms

class Tag(models.Model):
	tag_name = models.CharField('#tagname', max_length=50)
	date_pub = models.DateTimeField(auto_now_add=True)
	approve_status = models.BooleanField(default=False)
	author = models.ForeignKey(User)
	def __str__(self):              # __unicode__ on Python 2
		return self.tag_name
	@classmethod
	def create(cls, name, author):
		tag_obj = cls(tag_name=name, author=author)
		# do something with the picture
		return tag_obj

class Category(models.Model):
	category_name = models.CharField('Category name', max_length=75)
	date_pub = models.DateTimeField(auto_now_add=True)
	approve_status = models.BooleanField(default=False)
	author = models.ForeignKey(User)
	def __str__(self):              # __unicode__ on Python 2
		return self.category_name
	@classmethod
	def create(cls, name, author):
		cat_obj = cls(category_name=name, author=author)
		# do something with the picture
		return cat_obj
		

class Picture(models.Model):

	"""
	three size sets:
		thumbnail (photo_thumb)
		medium (photo_medium)
		original (photo_original)
	"""
	def path_and_rename(path):
		def wrapper(instance, filename):
			ext = filename.split('.')[-1]
			# get filename
			filename = '{}.{}'.format(uuid4().hex, ext)
			# return the whole path to the file
			return os.path.join(path, filename)
		return wrapper

	now = str(int(time.time()))
	filepath = 'gallery/'+hashlib.md5(now).hexdigest()+'/'

	picture_name = models.CharField('Name', max_length=100)
	date_pub = models.DateTimeField(auto_now_add=True, auto_now=True)
	approve_status = models.BooleanField(default=False)
	date_approve = models.DateTimeField(null=True)
	photo_origin = models.ImageField('original file upload', upload_to=path_and_rename(filepath))
	photo_medium = models.CharField(max_length=255, blank=True)
	photo_thumb = models.CharField(max_length=255, blank=True)
	category = models.ManyToManyField(Category, blank=True)
	tag = models.ManyToManyField(Tag, blank=True)
	author = models.ForeignKey(User)
	
	def __str__(self):
		return self.picture_name

	def get_thumb(self):
		return "/site_media/%s" % self.photo_thumb

	def get_medium(self):
		return "/site_media/%s" % self.photo_medium

	def get_original(self):
		return "/site_media/%s" % self.photo_origin

	def __iter__(self):
		return self

	@classmethod
	def create(cls, name, picture, user_added):
		image_obj = cls(picture_name=name, photo_origin=picture, author=user_added)
		# do something with the picture
		return image_obj

	def save(self):
		sizes = {'thumbnail': {'height': 240, 'width': 320}, 'medium': {'height': 480, 'width': 640},}

		super(Picture, self).save()
		if not self.photo_medium:
			photopath = str(self.photo_origin.path)  # this returns the full system path to the original file
			im = Image.open(photopath)  # open the image using PIL
			
		# pull a few variables out of that full path
			extension = photopath.rsplit('.', 1)[1]  # the file extension
			filename = photopath.rsplit('/', 1)[1].rsplit('.', 1)[0]  # the file name only (minus path or extension)
			fullpath = photopath.rsplit('/', 1)[0]  # the path only (minus the filename.extension)

			# use the file extension to determine if the image is valid before proceeding
			if extension not in ['jpg', 'jpeg', 'gif', 'png']: sys.exit()

			# create medium image
			im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
			#medname = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height']) + ".jpg"
			medname = uuid4().hex + ".jpg"
			im.save(fullpath + '/' + medname)
			self.photo_medium = self.filepath + medname

			# create thumbnail
			im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
			#thumbname = filename + "_" + str(sizes['thumbnail']['width']) + "x" + str(sizes['thumbnail']['height']) + ".jpg"
			thumbname = uuid4().hex + ".jpg"
			im.save(fullpath + '/' + thumbname)
			self.photo_thumb = self.filepath + thumbname

			super(Picture, self).save()

class Link(models.Model):
	link_name = models.CharField('Link name', max_length=25)
	link_url = models.URLField(max_length=200)
	date_pub = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	links = models.ManyToManyField(Link, blank=True)

class Organization(models.Model):
	org_name = models.CharField('Organization name', max_length=25)
	org_url = models.URLField(max_length=200)
	org_description = models.CharField('Description', max_length=4000)
	date_pub = models.DateTimeField(auto_now_add=True)
	links = models.ManyToManyField(Link, blank=True)

class Uploads(models.Model):
	date_pub = models.DateTimeField(auto_now_add=True)
	amount = models.FloatField()
	picture = models.ForeignKey(Picture, unique=True)
	organization = models.ForeignKey(Organization, unique=True)
	donator = models.CharField('Donator uiid', max_length=50)
	t_uuid = models.CharField('Transaction uiid', max_length=400)






	
