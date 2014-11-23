from care.models import Category, Download, Picture, UserProfile, Organization, Tag
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from django.utils import translation
from itertools import chain, groupby
from django.db.models import Count, Max, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.templatetags.static import static

def category_list(request):
	if request.method == 'GET':
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		translation.activate(request.GET.get('ln'))

		categories = []
		cat_list = Category.objects.filter(approve_status=True).annotate(count = Count('download')).order_by('-count')
		
		cat_on_page = 4
		paginator = Paginator(cat_list, cat_on_page)

		try:
			page = request.GET.get('page')
			try:
				cats = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				cats = paginator.page(1)
				page = 1
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				cats = paginator.page(paginator.num_pages)
				page = paginator.num_pages
			
			for cat in cats:
				category = {};
				category['id'] = cat.id
				category['name'] = cat.name
				category['downloads'] = cat.download_set.filter().count()
				#category['picture_url'] = cat.picture_set.filter(approve_status=True).annotate(count_d = Count('download')).order_by('-count_d')first().photo_thumb
				#p_cats = cat.picture_set
				#p_cats = p_cats.aggregate(Max('price'))
				pics = Picture.objects.filter(category=cat.id).annotate(count = Count('download')).order_by('-count').first().photo_thumb

				category['picture_url'] = pics

				categories.append(category)

			json_posts = json.dumps({'success':"true", 'message':'', 'page':page, 'count':paginator.num_pages, 'entity':categories})
			response = HttpResponse(json_posts, content_type="application/json")
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def popular_list(request):
	if request.method == 'GET':
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		translation.activate(request.GET.get('ln'))
		popular = []
		picture_list = Picture.objects.filter(approve_status=True).annotate(count = Count('download')).order_by('-count')
		
		picture_on_page = 4
		paginator = Paginator(picture_list, picture_on_page)

		try:
			page = request.GET.get('page')
			try:
				pictures = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				pictures = paginator.page(1)
				page = 1
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				pictures = paginator.page(paginator.num_pages)
				page = paginator.num_pages
			
			for pic in pictures:
				picture = {};
				picture['id'] = pic.id
				picture['downloads'] = pic.download_set.filter().count()
				picture['picture_url'] = pic.photo_thumb

				popular.append(picture)

			json_posts = json.dumps({'success':"true", 'message':'', 'page':page, 'count':paginator.num_pages, 'entity':popular})
			response = HttpResponse(json_posts, content_type="application/json")
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def picture_by_cat_list(request):
	if request.method == 'GET':
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		translation.activate(request.GET.get('ln'))
		
		if not request.GET.get('id'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide vaild id'}), content_type="application/json")
		
		c_id = int(request.GET.get('id'))

		popular = []
		try:
				
			page = request.GET.get('page')
			cat_id = int(c_id)

			picture_list = Picture.objects.filter(approve_status=True, category=cat_id).annotate(count = Count('download')).order_by('-count')

			picture_on_page = 4
			paginator = Paginator(picture_list, picture_on_page)

			try:
				pictures = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				pictures = paginator.page(1)
				page = 1
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				pictures = paginator.page(paginator.num_pages)
				page = paginator.num_pages
			
			for pic in pictures:
				picture = {};
				picture['id'] = pic.id
				picture['picture_url'] = pic.photo_thumb
				#picture['name'] = pic.picture_name

				popular.append(picture)
			cat = Category.objects.get(pk=cat_id).category_name
			json_posts = json.dumps({'success':"true", 'message':'', 'page':page, 'count':paginator.num_pages, 'page_name':cat, 'entity':popular})
			response = HttpResponse(json_posts, content_type="application/json")
		
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def picture(request):
	if request.method == 'GET':
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		translation.activate(request.GET.get('ln'))
		if not request.GET.get('id'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide vaild id'}), content_type="application/json")
		
		try:	
			pic_id = int(request.GET.get('id'))
			try:
				pic = Picture.objects.filter(approve_status=True).get(pk=pic_id)
			except:
				response = HttpResponse(json.dumps({'success':"false", 'message':"Wrong picture request..."}), content_type="application/json")
			finally:
				picture = {};
				picture['id'] = pic.id
				picture['downloads'] = pic.download_set.filter().count()
				picture['picture_url'] = pic.photo_medium
				picture['name'] = pic.picture_name
				usr = User.objects.get(pk=pic.author.id)
				picture['author'] = "%s %s" % (usr.first_name, usr.last_name)
				json_posts = json.dumps({'success':"true", 'message':'', 'entity':picture})
				response = HttpResponse(json_posts, content_type="application/json")
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def organizations(request):
	if request.method == 'GET':
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		translation.activate(request.GET.get('ln'))

		organizations = []
		org_list = Organization.objects.all() #.annotate(count = Count('download')).order_by('-count')

		try:			
			for org in org_list:
				organization = {};
				organization['id'] = org.id
				organization['name'] = org.name
				organization['description'] = org.description
				organization['author'] = org.author
				donated = Download.objects.filter(organization=org.id).aggregate(Sum('amount'))
				organization['amount'] = donated['amount__sum']
				organization['user_amount'] = 0

				organizations.append(organization)

			json_posts = json.dumps({'success':"true", 'message':'', 'entity':organizations})
			response = HttpResponse(json_posts, content_type="application/json")
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def search(request):
	if request.method == 'GET':
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		if not request.GET.get('param'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide search param'}), content_type="application/json")


		translation.activate(request.GET.get('ln'))
		pic_cat_list = {}
		pic_tag_list = {}
		pic_list = {}
		try:	

			pic_list = Picture.objects.filter(approve_status=True, translations__name__icontains=request.GET.get('param')) #.annotate(count = Count('download')).order_by('-count')

			cat_list = Category.objects.filter(approve_status=True, translations__name__icontains=request.GET.get('param'))
			
			pic_cat_list = {}
			if cat_list:
				for cat in cat_list:
					pic_cat_list = list(chain(pic_cat_list, Picture.objects.filter(approve_status=True, category=cat.id)))

			tag_list = Tag.objects.filter(approve_status=True, translations__name__icontains=request.GET.get('param'))

			if tag_list:
				for tag in tag_list:
					pic_tag_list = list(chain(pic_tag_list, Picture.objects.filter(approve_status=True, tag=tag.id)))

			pictures = list(chain(pic_list, pic_cat_list, pic_tag_list))

			unique_results = [rows.next() for (key, rows) in groupby(pictures, key=lambda obj: obj.id)]
			
			if unique_results:
				popular = []
				page = request.GET.get('page')

				picture_on_page = 4
				paginator = Paginator(unique_results, picture_on_page)

				try:
					pictures = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					pictures = paginator.page(1)
					page = 1
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					pictures = paginator.page(paginator.num_pages)
					page = paginator.num_pages
				
				for pic in pictures:
					picture = {};
					picture['id'] = pic.id
					picture['picture_url'] = pic.photo_thumb
					#picture['name'] = pic.picture_name

					popular.append(picture)
				json_posts = json.dumps({'success':"true", 'message':'', 'page':page, 'count':paginator.num_pages, 'page_name':request.GET.get('param'), 'entity':popular})
				response = HttpResponse(json_posts, content_type="application/json")
			else:
				response = HttpResponse(json.dumps({'success':"true", 'message':'There are no results...'}), content_type="application/json")
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

def download(request):
	if request.method == 'GET':
		response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
		if not request.GET.get('ln'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide language'}), content_type="application/json")

		translation.activate(request.GET.get('ln'))

		if not request.GET.get('id'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide vaild id'}), content_type="application/json")
		
		if not request.GET.get('org_id'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide organization id'}), content_type="application/json")

		if not request.GET.get('amount'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide amount'}), content_type="application/json")
		
		if not request.GET.get('user_id'):
			return HttpResponse(json.dumps({'success':"false", 'message':'Provide user id'}), content_type="application/json")

		#try:	
		pic_id = int(request.GET.get('id'))
		try:
			pic = Picture.objects.filter(approve_status=True).get(pk=pic_id)
		except:
			response = HttpResponse(json.dumps({'success':"false", 'message':"Wrong picture request..."}), content_type="application/json")
		finally:
			try:
				org = Organization.objects.get(pk=request.GET.get('org_id'))
				up = Download.create(request.GET.get('amount'), pic, org, request.GET.get('user_id'), "api-development");
				up.save()
				for cat in pic.category.all():
					up.category.add(Category.objects.get(pk=int(cat.id)))
				up.save()
				response = HttpResponse(open(pic.photo_origin.path, "rb").read(), content_type="image/jpg")
			except:
				response = HttpResponse(json.dumps({'success':"false", 'message':"Wrong organization in request..."}), content_type="application/json")
				
		#except:
			#response = HttpResponse(json.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'success':"false", 'message':'Only GET allowed'}), content_type="application/json")
	
	response["Access-Control-Allow-Origin"] = "*"  
	response["Access-Control-Allow-Methods"] = "POST, GET"  
	response["Access-Control-Max-Age"] = "1000"  
	response["Access-Control-Allow-Headers"] = "*"
	return response

