from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from care import models
from care.models import Picture, Category, Tag, LinkType, Link, UserProfile, Download, Organization
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
from django.db.models import Q

from care.forms import UserInfoForm, UploadPictureForm, CategoryForm, EditPictureForm

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
	#Development
	cat_list = []
	for pic in pictures:
		cat_list.append(Category.objects.get(pk=pic.id))
	#End development
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
		CATEGORY_CHOICES = [[x.id, x.category_name] for x in Category.objects.filter()]
		TAG_CHOICES = [[x.id, x.tag_name] for x in Tag.objects.filter()]
		form = UploadPictureForm(CATEGORY_CHOICES, TAG_CHOICES, request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			p_name = form.cleaned_data['picture_name']
			image = request.FILES['image']
			
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
		categories = Category.objects.filter(Q(approve_status=True) | Q(author=p_author))
		tags = Tag.objects.filter(Q(approve_status=True) | Q(author=p_author))
		CATEGORY_CHOICES = [[x.id, x.category_name] for x in categories]
		TAG_CHOICES = [[x.id, x.tag_name] for x in tags]
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
			CATEGORY_CHOICES = [[x.id, x.category_name] for x in Category.objects.filter()]
			TAG_CHOICES = [[x.id, x.tag_name] for x in Tag.objects.filter()]
			form = EditPictureForm(CATEGORY_CHOICES, TAG_CHOICES, request.POST, request.FILES)
			# check whether it's valid:
			if form.is_valid():
				# process the data in form.cleaned_data as required
				selected_image.picture_name = form.cleaned_data['picture_name']
				selected_image.save()
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
			CATEGORY_CHOICES = [[x.id, x.category_name] for x in categories]
			TAG_CHOICES = [[x.id, x.tag_name] for x in tags]
			form = EditPictureForm(CATEGORY_CHOICES, TAG_CHOICES, initial={
				'categories': categories,
				'tags' : tags,
				'picture_name': selected_image.picture_name,})
		

	return render(request, 'care/edit.html', {'form': form, 'limit_detected': limit_detected, 'img':selected_image,})


@login_required
def AddCategoryView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		category_send = data["category_name"]
		p_author = User.objects.get(username = request.user.username)
		date = datetime.date
		today_min = datetime.datetime.combine(date.today(), datetime.time.min)
		today_max = datetime.datetime.combine(date.today(), datetime.time.max)
		categories = Category.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
		if categories.count() > 14:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'You were added maximum count of categories per today. Try tomorrow!'}), content_type="application/json")	
		elif not category_send:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'There are no category name presented!'}), content_type="application/json")	
		elif len(category_send) < 3:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Category name too short ( minimum 3 symbols )'}), content_type="application/json")	
		elif len(category_send) > 75:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Category name too long ( maximum 75 symbols )'}), content_type="application/json")	
		else:
			cat = Category.create(category_send, p_author)
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
		p_author = User.objects.get(username = request.user.username)
		date = datetime.date
		today_min = datetime.datetime.combine(date.today(), datetime.time.min)
		today_max = datetime.datetime.combine(date.today(), datetime.time.max)
		tags = Tag.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
		if tags.count() > 14:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'You were added maximum count of tags per today. Try tomorrow!'}), content_type="application/json")	
		elif  not tag_send:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'There are no tag name presented!'}), content_type="application/json")	
		elif len(tag_send) < 3:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Tag name too short ( minimum 3 symbols )'}), content_type="application/json")	
		elif len(tag_send) > 75:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Tag name too long ( maximum 75 symbols )'}), content_type="application/json")	
		else:
			tag = Tag.create(tag_send, p_author)
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


@login_required
def AddLinkView(request):
	data = simplejson.loads(request.body)

	if data is not None:
		link_type = data["link_type"]
		link_url = data["link_url"]
		links = UserProfile.objects.filter(user=request.user)
		if links.count() > 9:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'You have maximum limit of links (10 links for user)'}), content_type="application/json")	
		elif not link_type:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Choose link type, please!'}), content_type="application/json")	
		elif not link_url:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'There are no url name presented!'}), content_type="application/json")	
		elif len(link_url) < 12:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Url too short!'}), content_type="application/json")	
		elif len(link_url) > 199:
			return HttpResponse(simplejson.dumps({'success':"False", 'message':'Url too long!'}), content_type="application/json")	
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
				return HttpResponse(simplejson.dumps({'success':"False", 'message':'Some error happen!'}), content_type="application/json")	
			
	else:
		#, "message" : "Invalid data received by server"
		return HttpResponse(simplejson.dumps({'success':"False", 'message':'There is an error! Please contact us, if you know why?'}), content_type="application/json")



###Development section
@login_required()
def AddUploadView(request, picture_id):
	picture = Picture.objects.get(pk=picture_id)
	organization = Organization.objects.get(pk=1)
	up = Download.create("0.99", picture, organization, "admin", "");
	up.save()
	for cat in picture.category.all():
		up.category.add(Category.objects.get(pk=int(cat.id)))
	up.save()

	return HttpResponse("Thank you, upload tracked!")

###End of developing section







