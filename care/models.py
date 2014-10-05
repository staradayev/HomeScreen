from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	tag_name = models.CharField('#tagname', max_length=50)
	date_pub = models.DateTimeField()
	approve_status = models.BooleanField(default=False)
	def __str__(self):              # __unicode__ on Python 2
		return self.tag_name

class Category(models.Model):
	category_name = models.CharField('Category name', max_length=75)
	date_pub = models.DateTimeField()
	approve_status = models.BooleanField(default=False)
	def __str__(self):              # __unicode__ on Python 2
		return self.category_name

class Picture(models.Model):
	picture_name = models.CharField('Name', max_length=100)
	date_pub = models.DateTimeField()
	approve_status = models.BooleanField(default=False)
	date_approve = models.DateTimeField()
	image_origin = models.ImageField()
	category = models.ManyToManyField(Category)
	tag = models.ManyToManyField(Tag)
	author = models.ForeignKey(User)

class UserProfile(models.Model):
     user = models.ForeignKey(User, unique=True)
	
		