from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from care import models
from care.models import Picture, Category, Tag
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render
import datetime
from django.utils import timezone
import autocomplete_light
from django.forms.formsets import formset_factory
import json as simplejson

from care.forms import UserInfoForm, UploadPictureForm, CategoryForm

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

	picture_list = Picture.objects.order_by('-date_pub').all()
	pictures_all_count = picture_list.count()
	pictures_on_page = 4
	paginator = Paginator(picture_list, pictures_on_page)

	page = request.GET.get('page')
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		pictures = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		pictures = paginator.page(paginator.num_pages)

	template = loader.get_template('care/detail.html')
	context = RequestContext(request, {
		'picture_list': pictures,
		'allowed_count': pictures_on_page,
		'all_count': pictures_all_count,
	})
	return HttpResponse(template.render(context))

@login_required
def InfoView(request):
	name_empty = False
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
		name_empty = False
		if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
			name_empty = True
		user = User.objects.get(username = request.user.username)
		form = UserInfoForm(initial={
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email' : user.email,
			})

	return render(request, 'care/myinfo.html', {'form': form, 'name_empty': name_empty,})

@login_required()
def UploadView(request):
	if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
		return HttpResponseRedirect('/care/myinfo')

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		CATEGORY_CHOICES = [[x.id, x.category_name] for x in Category.objects.filter()]
		TAG_CHOICES = [[x.id, x.tag_name] for x in Tag.objects.filter()]
		form = UploadPictureForm(CATEGORY_CHOICES, TAG_CHOICES, request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			p_name = form.cleaned_data['picture_name']
			image = request.FILES['image']
			
			p_author = User.objects.get(username = request.user.username)
			pic = Picture.create(p_name, image, p_author)
			pic.save()
			for cat in form.cleaned_data['categories']:
				pic.category.add(Category.objects.get(pk=int(cat)))
			for t in form.cleaned_data['tags']:
				pic.tag.add(Tag.objects.get(pk=int(t)))

			pic.save()
			
			return HttpResponseRedirect('/care/detail')

	# if a GET (or any other method) we'll create a blank form
	else:
		categories = Category.objects.filter(approve_status=True)
		tags = Tag.objects.filter(approve_status=True)
		CATEGORY_CHOICES = [[x.id, x.category_name] for x in categories]
		TAG_CHOICES = [[x.id, x.tag_name] for x in tags]
		form = UploadPictureForm(CATEGORY_CHOICES, TAG_CHOICES, initial={
			'categories': categories,
			'tags' : tags,})
		

	return render(request, 'care/upload.html', {'form': form})

@login_required
def AddCategoryView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		category_send = data["category_name"]
		if not category_send:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'There are no category name presented!'}), content_type="application/json")	
		elif len(category_send) < 3:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Category name too short ( minimum 3 symbols )'}), content_type="application/json")	
		elif len(category_send) > 75:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Category name too long ( maximum 75 symbols )'}), content_type="application/json")	
		else:
			cat = Category.create(category_send)
			cat.save()
			response_data = {}
			response_data['success'] = 'true'
			response_data['name'] = cat.category_name
			response_data['val'] = cat.id
		
			#, "data" : dataReturn
			return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':'There is an error! Please contact us, if you know why?'}), content_type="application/json")

@login_required
def AddTagView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		tag_send = data["tag_name"]
		if not tag_send:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'There are no tag name presented!'}), content_type="application/json")	
		elif len(tag_send) < 3:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Tag name too short ( minimum 3 symbols )'}), content_type="application/json")	
		elif len(tag_send) > 75:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Tag name too long ( maximum 75 symbols )'}), content_type="application/json")	
		else:
			tag = Tag.create(tag_send)
			tag.save()
			response_data = {}
			response_data['success'] = 'true'
			response_data['name'] = tag.tag_name
			response_data['val'] = tag.id
		
			#, "data" : dataReturn
			return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':'There is an error! Please contact us, if you know why?'}), content_type="application/json")








