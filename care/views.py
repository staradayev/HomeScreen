from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from care import models
from care.models import Picture, PictureTranslation, Category, CategoryTranslation, Tag, TagTranslation, LinkType, Link, UserProfile, Download, Organization
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render
import datetime
from django.utils import timezone, translation
from django.forms.formsets import formset_factory
import json as simplejson
from django.db.models import Q, Count
from django.utils.translation import ugettext as _
from care.forms import UserInfoForm, UploadPictureForm, CategoryForm, EditPictureForm
import urllib
from unidecode import unidecode
from django.core.urlresolvers import reverse
import os
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse, UploadResponseError
from django.conf import settings
from django.core.files.images import get_image_dimensions
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.utils import formats

def logout(request, redirect_url=None):
	auth.logout(request)
	return HttpResponseRedirect('/care/loggedout')

def loggedout(request):
	template = loader.get_template('care/loggedout.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

@login_required
def logged(request):
	return HttpResponse("You are logged user")

@login_required
def DetailView(request):
	if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
		return HttpResponseRedirect('/care/myinfo')

	p_author = User.objects.get(username = request.user.username)
	picture_list = Picture.objects.filter(author=p_author).order_by('-date_pub').all()
	pictures_all_count = picture_list.count()


	template = loader.get_template('care/detail.html')
	context = RequestContext(request, {
		'picture_list': picture_list,
		'all_count': pictures_all_count,
	})
	return HttpResponse(template.render(context))

@login_required
def InfoView(request):
	name_empty = False
	link_types = None
	user_links = None
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserInfoForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			user = User.objects.get(username = request.user.username)
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.email = form.cleaned_data['email']
			user.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/care/detail')

	# if a GET (or any other method) we'll create a blank form
	else:
		if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
			name_empty = True
		user = User.objects.get(username = request.user.username)
		form = UserInfoForm(initial={
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email' : user.email,
			})
		link_types = LinkType.objects.all()

		user_p = None

		try:
			user_p = UserProfile.objects.get(user=user)
		except Exception, e:
			up = UserProfile.create(user)
			up.user = user
			up.save()
			user_p = UserProfile.objects.get(user=user)
		finally:
			user_links = user_p.links			

	return render(request, 'care/myinfo.html', {'form': form, 'name_empty': name_empty,'link_types':link_types, 'user_links': user_links,})

@login_required()
def UploadView(request):
	if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
		return HttpResponseRedirect('/care/myinfo')

	limit_detected = False
	p_author = User.objects.get(username = request.user.username)
	date = datetime.date
	today_min = datetime.datetime.combine(date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(date.today(), datetime.time.max)
	pics = Picture.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
	if pics.count() > 9:
		limit_detected = True


	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		CATEGORY_CHOICES = [[x.id, x.name] for x in Category.objects.filter()]
		TAG_CHOICES = [[x.id, x.name] for x in Tag.objects.filter()]
		form = UploadPictureForm(CATEGORY_CHOICES, TAG_CHOICES, request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			p_name = form.cleaned_data['name']
			image = request.FILES['image']
			
			pic = Picture.create(image, p_author)
			pic.save()

			pic_trans = PictureTranslation(language_code=translation.get_language())
			pic_trans.name = p_name
			pic_trans.parent = pic
			pic_trans.save()

			for cat in form.cleaned_data['categories']:
				pic.category.add(Category.objects.get(pk=int(cat)))
			for t in form.cleaned_data['tags']:
				pic.tag.add(Tag.objects.get(pk=int(t)))

			pic.save()
			
			return HttpResponseRedirect('/care/detail')

	# if a GET (or any other method) we'll create a blank form
	else:
		categories = Category.objects.filter(Q(approve_status=True) | Q(author=p_author))
		tags = Tag.objects.filter(Q(approve_status=True) | Q(author=p_author))
		CATEGORY_CHOICES = [[x.id, x.name] for x in categories]
		TAG_CHOICES = [[x.id, x.name] for x in tags]
		form = UploadPictureForm(CATEGORY_CHOICES, TAG_CHOICES, initial={
			'categories': categories,
			'tags' : tags,})
		

	return render(request, 'care/upload.html', {'form': form, 'limit_detected': limit_detected,})

@login_required()
def EditView(request, picture_id):
	if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
		return HttpResponseRedirect('/care/myinfo')
	selected_image = None
	limit_detected = False
	p_author = User.objects.get(username = request.user.username)
	try:
		selected_image = Picture.objects.get(Q(pk=picture_id), Q(approve_status=False), Q(author=p_author))
	except (KeyError, Picture.DoesNotExist):
		return render(request, 'care/edit.html', {
				'limit_detected': True,
			})
	else:
		# if this is a POST request we need to process the form data
		if request.method == 'POST':
			# create a form instance and populate it with data from the request:
			CATEGORY_CHOICES = [[x.id, x.name] for x in Category.objects.filter()]
			TAG_CHOICES = [[x.id, x.name] for x in Tag.objects.filter()]
			form = EditPictureForm(CATEGORY_CHOICES, TAG_CHOICES, request.POST, request.FILES)
			# check whether it's valid:
			if form.is_valid():
				# process the data in form.cleaned_data as required
				selected_image.save()
				image_trans = PictureTranslation.objects.get(parent_id=selected_image.id)
				image_trans.name = form.cleaned_data['name']
				image_trans.save()

				for cat in form.cleaned_data['categories']:
					selected_image.category.add(Category.objects.get(pk=int(cat)))
				for t in form.cleaned_data['tags']:
					selected_image.tag.add(Tag.objects.get(pk=int(t)))

				selected_image.save()
				
				return HttpResponseRedirect('/care/')

		# if a GET (or any other method) we'll create a blank form
		else:
			categories = Category.objects.filter(Q(approve_status=True) | Q(author=p_author))
			tags = Tag.objects.filter(Q(approve_status=True) | Q(author=p_author))
			CATEGORY_CHOICES = [[x.id, x.name] for x in categories]
			TAG_CHOICES = [[x.id, x.name] for x in tags]
			form = EditPictureForm(CATEGORY_CHOICES, TAG_CHOICES, initial={
				'categories': categories,
				'tags' : tags,
				'name': selected_image.name,})
		

	return render(request, 'care/edit.html', {'form': form, 'limit_detected': limit_detected, 'img':selected_image,})


@login_required
def AddCategoryView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		category_send = urllib.url2pathname(unidecode(data["category_name"]))
		print category_send
		p_author = User.objects.get(username = request.user.username)
		date = datetime.date
		today_min = datetime.datetime.combine(date.today(), datetime.time.min)
		today_max = datetime.datetime.combine(date.today(), datetime.time.max)
		categories = Category.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
		if categories.count() > 14:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"You were added maximum count of categories per today. Try tomorrow!")}), content_type="application/json")	
		elif not category_send:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There are no category name presented!")}), content_type="application/json")	
		elif len(category_send) < 3:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Category name too short ( minimum 3 symbols )")}), content_type="application/json")	
		elif len(category_send) > 75:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Category name too long ( maximum 75 symbols )")}), content_type="application/json")	
		else:
			cat = Category.create(p_author)
			cat.save()
			category_trans = CategoryTranslation(language_code=translation.get_language())
			category_trans.name = category_send.decode('utf-8')
			category_trans.parent = cat
			category_trans.save()
			response_data = {}
			response_data['success'] = 'true'
			response_data['name'] = cat.name
			response_data['val'] = cat.id
		
			#, "data" : dataReturn
			return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")

@login_required
def AddTagView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		tag_send = urllib.url2pathname(unidecode(data["tag_name"]))
		print tag_send
		p_author = User.objects.get(username = request.user.username)
		date = datetime.date
		today_min = datetime.datetime.combine(date.today(), datetime.time.min)
		today_max = datetime.datetime.combine(date.today(), datetime.time.max)
		tags = Tag.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
		if tags.count() > 14:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"You were added maximum count of tags per today. Try tomorrow!")}), content_type="application/json")	
		elif  not tag_send:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There are no tag name presented!")}), content_type="application/json")	
		elif len(tag_send) < 3:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Tag name too short ( minimum 3 symbols )")}), content_type="application/json")	
		elif len(tag_send) > 75:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Tag name too long ( maximum 75 symbols )")}), content_type="application/json")	
		else:
			tag = Tag.create(p_author)
			tag.save()
			tag_trans = TagTranslation(language_code=translation.get_language())
			tag_trans.name = tag_send.decode('utf-8')
			tag_trans.parent = tag
			tag_trans.save()
			response_data = {}
			response_data['success'] = 'true'
			response_data['name'] = tag.name
			response_data['val'] = tag.id
		
			#, "data" : dataReturn
			return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@login_required
def AddLinkView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		link_type = data["link_type"]
		link_url = data["link_url"]
		links = UserProfile.objects.filter(user=request.user)
		if links.count() > 9:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"You have maximum limit of links (10 links for user)")}), content_type="application/json")	
		elif not link_type:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Choose link type, please!")}), content_type="application/json")	
		elif not link_url:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There are no url name presented!")}), content_type="application/json")	
		elif len(link_url) < 5:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Url too short!")}), content_type="application/json")	
		elif len(link_url) > 199:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Url too long!")}), content_type="application/json")	
		else:
			try:

				l_type = LinkType.objects.get(id=link_type)
				lnk = Link.create(l_type)
				lnk.link_url = link_url
				lnk.save()
				up = UserProfile.objects.get(user=request.user)
				up.links.add(lnk)
				response_data = {}
				response_data['success'] = 'true'
				response_data['type'] = LinkType.objects.get(id=l_type.id).type_tag
				response_data['val'] = lnk.link_url
			
				#, "data" : dataReturn
				return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
			except:
				return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")	
			
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")



###Development section
@login_required()
def AddUploadView(request, picture_id):
	picture = Picture.objects.get(pk=picture_id)
	organization = Organization.objects.get(pk=1)
	up = Download.create("0.99", picture, organization, "admin", "care-development");
	up.save()
	for cat in picture.category.all():
		up.category.add(Category.objects.get(pk=int(cat.id)))
	up.save()

	return HttpResponse("Thank you, upload tracked!")

###End of developing section
@csrf_exempt
def upload_thumb( request ):
	data = simplejson.loads(request.body)
	pic = {}
	if data is not None:
		try:
			pic = Picture.objects.get(pk=data["pic_id"])
			im = Image.open(pic.photo_origin.path)
			w, h = im.size
			#'try crop and save'
			im.crop((int(w*data["left"]), int(h*data["top"]), int(w*data["right"]), int(h*data["bottom"]))).save(settings.MEDIA_ROOT + pic.photo_thumb)
			#'try open and resize'
			img = Image.open(settings.MEDIA_ROOT + pic.photo_thumb).resize( (240, 240) )
			#'try save'
			img.save(settings.MEDIA_ROOT + pic.photo_thumb)
			#settings.MEDIA_ROOT + pic.photo_thumb
			#'saved'
			response_data = {}
			response_data['success'] = 'true'
			response_data['id'] = pic.id
		
			#, "data" : dataReturn
			return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
		except:
			return HttpResponse(simplejson.dumps({'success':"false", 'message':"Wrong picture request..."}), content_type="application/json")			
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@login_required()
def upload_description( request ):
	data = simplejson.loads(request.body)
	selected_image = None
	if data is not None:
		try:
			p_author = User.objects.get(username = request.user.username)
			if not data["pic_id"]:
				return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Provide picture...")}), content_type="application/json")	
			
			try:
				selected_image = Picture.objects.get(Q(pk=data["pic_id"]), Q(approve_status=False), Q(author=p_author))
			except (KeyError, Picture.DoesNotExist):
				return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Picture is wrong")}), content_type="application/json")

			name = ""
			if not data["pic_name"]:
				return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Picture name is required")}), content_type="application/json")	
			elif len(data["pic_name"]) < 2:
				return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Picture name too short!")}), content_type="application/json")	
			elif len(data["pic_name"]) > 99:
				return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"Picture name too long!")}), content_type="application/json")	
			else:
				name = urllib.url2pathname(unidecode(data["pic_name"]))

			pic_trans = None
			try:
				pic_trans = PictureTranslation.objects.get(parent_id=selected_image.id)
			except (KeyError, PictureTranslation.DoesNotExist):
				pic_trans = PictureTranslation(language_code=translation.get_language())
			finally:
				pic_trans.name = name.decode('utf-8')
				pic_trans.parent = selected_image
				pic_trans.save()

			if data["pic_cats"]:
				for cat in data["pic_cats"]:
					selected_image.category.add(Category.objects.get(pk=int(cat)))
			if data["pic_tags"]:		
				for t in data["pic_tags"]:
					selected_image.tag.add(Tag.objects.get(pk=int(t)))

			if data["pic_cats"] or data["pic_tags"]:
				selected_image.save()
			
			return HttpResponse(simplejson.dumps({'success':"true", 'message':"Saved success!"}), content_type="application/json")
		except:
			response = HttpResponse(simplejson.dumps({'success':"false", 'message':"Wrong picture request..."}), content_type="application/json")			
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':_(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@require_POST
def UploadPictureView( request ):

	# The assumption here is that jQuery File Upload
	# has been configured to send files one at a time.
	# If multiple files can be uploaded simulatenously,
	# 'file' may be a list of files.
	file = upload_receive( request )

	p_author = User.objects.get(username = request.user.username)

	image = file

	if not image:
		return UploadResponseError( request, {
			"error": (_(u"No image!")),
			"url": "", 
			"thumbnail_url": "", 
			"delete_url": "", 
			"delete_type": "DELETE", 
			"name": '', 
			"size": ''
		})
	else:
		from django.core.files.images import get_image_dimensions
		w, h = get_image_dimensions(image)

		#validate dimensions
		mwidth = 1920 
		mheight = 1080
		if (w > h and (w < mwidth or h < mheight)) or (w < h and (h < mwidth or w < mheight)):
			return UploadResponseError( request, {
				"error": (_(u"Too low image size, please use bigger!")),
				"url": "", 
				"thumbnail_url": "", 
				"delete_url": "", 
				"delete_type": "DELETE", 
				"name": '', 
				"size": ''
			})
		#portaint or landscape max size check
		if (w > h and (w > mwidth*5 or h > mheight*5)) or (w < h and (h > mwidth*5 or w > mheight*5)):
			return UploadResponseError( request, {
				"error": (_(u"Too big image size! Please use smaller.")),
				"url": "", 
				"thumbnail_url": "", 
				"delete_url": "", 
				"delete_type": "DELETE", 
				"name": '', 
				"size": ''
			})

		#validate content type
		main, sub = image.content_type.split('/')
		if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
			return UploadResponseError( request, {
				"error": (_(u'Please use a JPEG or PNG image.')),
				"url": "", 
				"thumbnail_url": "", 
				"delete_url": "", 
				"delete_type": "DELETE", 
				"name": '', 
				"size": ''
			})

		#validate file size
		if len(image) > (10 * 1024 * 1024):
			return UploadResponseError( request, {
				"error": (_(u'Image file too large')),
				"url": "", 
				"thumbnail_url": "", 
				"delete_url": "", 
				"delete_type": "DELETE", 
				"name": '', 
				"size": ''
			})
				



	instance = Picture.create(file, p_author)
	instance.save()

	basename = os.path.basename( instance.photo_origin.path )

	file_dict = {
		'name' : basename,
		'size' : file.size,

		'url': instance.photo_origin.url,
		'thumbnailUrl': instance.photo_origin.url,

		'deleteUrl': reverse('care:jfu_delete', kwargs = { 'pk': instance.pk }),
		'deleteType': 'POST',
		'id' : instance.id
	}

	return UploadResponse( request, file_dict )

@require_POST
def upload_delete( request, pk ):
	success = True
	try:
		instance = Picture.objects.get( pk = pk )
		os.unlink( instance.photo_origin.path )
		instance.delete()
	except Picture.DoesNotExist:
		success = False

	return JFUResponse( request, success )

def GetCategoryView(request):
	if request.method == 'GET':
		if not request.GET.get('query'):
			return HttpResponse(simplejson.dumps({'success':"false", 'message':'Provide query'}), content_type="application/json")

		p_author = User.objects.get(username = request.user.username)
		categories = []
		cats = Category.objects.filter(Q(approve_status=True) | Q(author=p_author) | Q(translations__name__icontains=request.GET.get('query'))).annotate(count = Count('download')).order_by('-count')

		#try:
		if cats:
			for cat in cats:
				category = {};
				category['id'] = cat.id
				category['name'] = cat.name
				#pics = Picture.objects.filter(category=cat.id).annotate(count = Count('download')).order_by('-count').first().photo_thumb

				#category['picture_url'] = pics

				categories.append(category)

		json_posts = simplejson.dumps({'success':"true", 'message':'', 'entity':categories})
		response = HttpResponse(json_posts, content_type="application/json")
		#except:
			#response = HttpResponse(simplejson.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(simplejson.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def GetTagView(request):
	if request.method == 'GET':
		if not request.GET.get('query'):
			return HttpResponse(simplejson.dumps({'success':"false", 'message':'Provide query'}), content_type="application/json")

		p_author = User.objects.get(username = request.user.username)
		res_tags = []
		tags = Tag.objects.filter(Q(approve_status=True) | Q(author=p_author) | Q(translations__name__icontains=request.GET.get('query')))

		#try:
		if tags:
			for t in tags:
				tag = {};
				tag['id'] = t.id
				tag['name'] = t.name

				res_tags.append(tag)

		json_posts = simplejson.dumps({'success':"true", 'message':'', 'entity':res_tags})
		response = HttpResponse(json_posts, content_type="application/json")
		#except:
			#response = HttpResponse(simplejson.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(simplejson.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def get_picture_list(request):
	if request.method == 'GET':

		pictures = []

		p_author = User.objects.get(username = request.user.username)
		picture_list = Picture.objects.filter(author=p_author).order_by('-date_pub').all()
		pictures_all_count = picture_list.count()
		pictures_on_page = 4
		paginator = Paginator(picture_list, pictures_on_page)


		template = loader.get_template('care/detail.html')
		context = RequestContext(request, {
			'picture_list': pictures,
			'allowed_count': pictures_on_page,
			'all_count': pictures_all_count,
		})

		try:
			page = request.GET.get('page')
			try:
				pics = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				pics = paginator.page(1)
				page = 1
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				pics = paginator.page(paginator.num_pages)
				page = paginator.num_pages
			
			for pic in pics:
				picture = {};
				picture['id'] = pic.id
				picture['name'] = pic.name
				picture['downloads'] = pic.download_set.filter().count()

				picture['thumb_url'] = pic.get_thumb()
				picture['preview_url'] = pic.get_medium()
				picture['author'] = "%s %s" % (p_author.first_name, p_author.last_name)
				picture['published'] = formats.date_format(pic.date_pub, "SHORT_DATETIME_FORMAT")
				if pic.date_approve:
					picture['approve'] = formats.date_format(pic.date_approve, "SHORT_DATETIME_FORMAT")


				if pic.category.all():
					picture['cats'] = []
					p_cats = pic.category.all()
					for cat in p_cats:
						category = {};
						category['id'] = cat.id
						category['name'] = cat.name
						picture['cats'].append(category)

				if pic.tag.all():
					picture['tags'] = []
					p_tags = pic.tag.all()
					for tag in p_tags:
						t = {};
						t['id'] = tag.id
						t['name'] = tag.name
						picture['tags'].append(t)

				if pic.download_count():
					picture['downloads'] = pic.download_count()

				pictures.append(picture)

			json_posts = simplejson.dumps({'success':"true", 'message':'', 'page':page, 'count':paginator.num_pages, 'entity':pictures})
			response = HttpResponse(json_posts, content_type="application/json")
		except:
			response = HttpResponse(simplejson.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(simplejson.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

