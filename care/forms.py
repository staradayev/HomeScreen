from care import models
from care.models import Picture, Category, Tag
from django import forms
import datetime
from django.utils import timezone
from PIL import Image
from django.utils.translation import ugettext as _

class UserInfoForm(forms.Form):
	def clean_first(value):
		fname = value
		if not fname:
			raise forms.ValidationError(_(u"There are no first name presented!"))
		elif len(fname) < 4:
			raise forms.ValidationError(_(u"First name too short ( minimum 4 symbols )"))
		elif len(fname) > 20:
			raise forms.ValidationError(_(u"First name too long ( maximum 20 symbols )"))
		return value
	def clean_last(value):
		lname = value
		if not lname:
			raise forms.ValidationError(_(u"There are no last name presented!"))
		elif len(lname) < 4:
			raise forms.ValidationError(_(u"Last name too short ( minimum 4 symbols )"))
		elif len(lname) > 20:
			raise forms.ValidationError(_(u"Last name too long ( maximum 20 symbols )"))
		return value
	def clean_mail(value):
		lname = value
		if not lname:
			raise forms.ValidationError(_(u"There are no email presented!"))
		elif len(lname) < 9:
			raise forms.ValidationError(_(u"mail name too short ( minimum 9 symbols )"))
		elif len(lname) > 100:
			raise forms.ValidationError(_(u"Email too long ( maximum 100 symbols )"))
		return value

	email = forms.EmailField(validators=[clean_mail], label="e-mail")
	first_name = forms.CharField(max_length=30, validators=[clean_first], label="First name")
	last_name = forms.CharField(max_length=30, validators=[clean_last], label="Last name")

class UploadPictureForm(forms.Form):
	def __init__(self, cat_choices, tag_choices, *args, **kwargs):
		super(UploadPictureForm, self).__init__(*args, **kwargs)
		self.fields["categories"] = forms.MultipleChoiceField(choices=cat_choices, required=False)
		self.fields["tags"] = forms.MultipleChoiceField(choices=tag_choices, required=False)

	def clean_picture(self):
		image = self

		if not image:
			raise forms.ValidationError((_(u"No image!")))
		else:
			from django.core.files.images import get_image_dimensions
			w, h = get_image_dimensions(image)
			
			#validate dimensions
			mwidth = 1920 
			mheight = 1080
			if w < mwidth or h < mheight:
				raise forms.ValidationError((_(u"Please use an image that is smaller or equal to %(width) x %(height) pixels..") 
					% {'width': mwidth, 'height': mheight}))
			if w > mwidth*4 or h > mheight*4:
				raise forms.ValidationError((_(u"Please use an image that is smaller or equal to %(width) x %(height) pixels..")
					% {'width': mwidth*4, 'height': mheight*4}))

			#validate content type
			main, sub = image.content_type.split('/')
			if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
				raise forms.ValidationError((_(u'Please use a JPEG or PNG image.')))

			#validate file size
			if len(image) > (8 * 1024 * 1024):
				raise forms.ValidationError((_(u'Image file too large ( maximum 8mb )')))
		return self	

	CATEGORY_CHOICES = [[x.id, x.name] for x in Category.objects.filter(approve_status=True)]
	TAG_CHOICES = [[x.id, x.name] for x in Tag.objects.filter(approve_status=True)]
	#TEST_CHOICES.insert(0, ['', "Empty"])
	name = forms.CharField(max_length=100)
	image = forms.ImageField(validators=[clean_picture])
	categories = forms.MultipleChoiceField(required=False, choices=CATEGORY_CHOICES)
	tags = forms.MultipleChoiceField(required=False, choices=TAG_CHOICES)
	class Meta: 
		model = Picture

class EditPictureForm(forms.Form):
	def __init__(self, cat_choices, tag_choices, *args, **kwargs):
		super(EditPictureForm, self).__init__(*args, **kwargs)
		self.fields["categories"] = forms.MultipleChoiceField(choices=cat_choices, required=False)
		self.fields["tags"] = forms.MultipleChoiceField(choices=tag_choices, required=False)

	CATEGORY_CHOICES = [[x.id, x.name] for x in Category.objects.filter(approve_status=True)]
	TAG_CHOICES = [[x.id, x.name] for x in Tag.objects.filter(approve_status=True)]
	#TEST_CHOICES.insert(0, ['', "Empty"])
	name = forms.CharField(max_length=100)
	categories = forms.MultipleChoiceField(required=False, choices=CATEGORY_CHOICES)
	tags = forms.MultipleChoiceField(required=False, choices=TAG_CHOICES)
	class Meta: 
		model = Picture  

class CategoryForm(forms.Form):
	def clean_name(value):
		fname = value
		if not fname:
			raise forms.ValidationError(_(u"There are no category name presented!"))
		elif len(fname) < 3:
			raise forms.ValidationError(_(u'Category name too short ( minimum 3 symbols )'))
		elif len(fname) > 75:
			raise forms.ValidationError(_(u'Category name too long ( maximum 75 symbols )'))
		return value
	category_name = forms.CharField(validators=[clean_name])





