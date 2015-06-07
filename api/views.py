from django.views.generic.base import View
from django.http import JsonResponse
from care.models import Category, Download, Picture, Organization, Tag, UserProfile, Like
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import translation
from itertools import chain, groupby
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from validate_email import validate_email
from django.conf import settings
from operator import itemgetter
import urllib2
import json



class BaseMixin(View):
    http_method_names = ['get']

    def http_method_not_allowed(self, request):
        return JsonResponse({'success': "false", 'message': 'Only GET allowed'})

    def dispatch(self, request):
        self.language = request.GET.get('ln')
        self.page_number = request.GET.get('page')
        self.id = request.GET.get('id')
        self.user = request.GET.get('user')
        self.user_id = request.GET.get('user_id')
        self.user_uid = request.GET.get('user_uid')
        self.org_id = request.GET.get('org_id')
        self.amount = request.GET.get('amount')
        self.param = request.GET.get('param')
        return super(BaseMixin, self).dispatch(request)

    def check_params(self, request, params_list):
        for param in params_list:
            if request.GET.get(param) is None:
                return JsonResponse({'success': "false", 'message': "Please provide " + param})
            elif self.language and param == 'ln':
                translation.activate(self.language)
            elif request.GET.get(param) and param == 'page':
                if not isinstance(self.page_number, (int, long)):
                    try:
                        self.page_number = int(self.page_number)
                    except:
                        self.page_number = 1
            elif request.GET.get(param) and param == 'user_id':
                if not validate_email(request.GET.get(param), verify=False):
                    return JsonResponse({'success': "false", 'message': "Please provide valid " + param})


class CategoryListView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page'])
        if check_result:
            return check_result
        categories_queryset = Category.objects.filter(approve_status=True).annotate(count=Count('download')).order_by('-count')
        paginator = Paginator(categories_queryset, settings.CATEGORIES_PER_PAGE)
        if self.page_number <= paginator.num_pages:
            page = self.page_number
        else:
            page = paginator.num_pages
        categories_paginated = paginator.page(page)
        categories = []
        for category_item in categories_paginated:
            category = {
                'id': category_item.id,
                'name': category_item.name,
                'downloads': category_item.download_set.all().count()
            }
            pic = Picture.objects.filter(category=category_item.id, approve_status=True).annotate(count=Count('download')).order_by('-count').first()
            pictures_queryset = Picture.objects.filter(category=category_item.id, approve_status=True)
            if pic is not None:
                category['picture_url'] = pic.photo_thumb
                category['picture_big_url'] = pic.photo_big_thumb
                category['pictures_count'] = pictures_queryset.count()
                categories.append(category)
        return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': categories})


class PopularListView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page'])
        if check_result:
            return check_result
        else:
            pictures_queryset = Picture.objects.filter(approve_status=True).annotate(count=Count('download')).order_by('-count')
            paginator = Paginator(pictures_queryset, settings.PICTURES_PER_PAGE)
            if self.page_number <= paginator.num_pages:
                page = self.page_number
            else:
                page = paginator.num_pages
            pictures_paginated = paginator.page(page)
            pictures = []
            for picture_item in pictures_paginated:
                picture = {
                    'id': picture_item.id,
                    'picture_url': picture_item.photo_thumb,
                    'picture_big_url': picture_item.photo_big_thumb,
                    'name': picture_item.name,
                    'downloads': picture_item.download_set.all().count(),
                    'likes': picture_item.like_set.filter().count(),
                }
                user = User.objects.get(pk=picture_item.author.id)
                picture['author'] = "%s %s" % (user.first_name, user.last_name)
                picture['author_id'] = user.id
                aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                picture['amount'] = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    picture['author_thumbnail'] = user_profile.get_thumb()
                    picture['author_photo'] = user_profile.get_user_picture()
                except Exception, e:
                    picture['author_thumbnail'] = None
                    picture['author_photo'] = None
                pictures.append(picture)
            return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures})


class PictureByCategoryListView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page', 'id'])
        if check_result:
            return check_result
        else:
            pictures_queryset = Picture.objects.filter(approve_status=True, category=self.id).annotate(count=Count('download')).order_by('-count')
            cat = Category.objects.get(pk=self.id)
            if pictures_queryset:
                paginator = Paginator(pictures_queryset, settings.PICTURES_PER_PAGE)
                if self.page_number <= paginator.num_pages:
                    page = self.page_number
                else:
                    page = paginator.num_pages
                pictures_paginated = paginator.page(page)
                pictures = []
                for picture_item in pictures_paginated:
                    picture = {
                        'id': picture_item.id,
                        'picture_url': picture_item.photo_thumb,
                        'picture_big_url': picture_item.photo_big_thumb,
                        'name': picture_item.name,
                        'downloads': picture_item.download_set.all().count(),
                        'likes': picture_item.like_set.filter().count(),
                    }
                    user = User.objects.get(pk=picture_item.author.id)
                    picture['author'] = "%s %s" % (user.first_name, user.last_name)
                    picture['author_id'] = user.id
                    aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                    picture['amount'] = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                    try:
                        user_profile = UserProfile.objects.get(user=user)
                        picture['author_thumbnail'] = user_profile.get_thumb()
                        picture['author_photo'] = user_profile.get_user_picture()
                    except Exception, e:
                        picture['author_thumbnail'] = None
                        picture['author_photo'] = None
                    pictures.append(picture)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures, 'page_name': cat.name})
            else:
                return JsonResponse({'success': "false", 'message': "No result for this id"})


class PictureView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'id'])
        if check_result:
            return check_result
        else:
            try:
                picture_queryset = Picture.objects.filter(approve_status=True).get(pk=self.id)
                user = User.objects.get(pk=picture_queryset.author.id)
                user_profile = UserProfile.objects.get(user=user)
                aggregation = Download.objects.filter(picture=picture_queryset.id).aggregate(price=Sum('amount'))
                donated = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                links = []
                liked = 'false'
                if request.GET.get('user_id') is not None and picture_queryset.like_set.filter(user=request.GET.get('user_id')).count() > 0:
                    liked = 'true'
                for link in user_profile.links.all():
                    lnk = {}
                    lnk['link_url'] = link.link_url
                    lnk['link_type'] = link.link_type.type_tag
                    links.append(lnk)
                categories = []
                for cat in picture_queryset.category.all():
                    pic = Picture.objects.filter(category=cat, approve_status=True).annotate(count=Count('download')).order_by('-count').first()
                    if pic is not None:
                        c = {}
                        c['name'] = cat.name
                        c['id'] = cat.id
                        c['picture_url'] = pic.photo_thumb
                        categories.append(c)
                tags = []
                for tag in picture_queryset.tag.all():
                    pic = Picture.objects.filter(tag=tag, approve_status=True).annotate(count=Count('download')).order_by('-count').first()
                    if pic is not None:
                        t = {}
                        t['name'] = tag.name
                        t['id'] = tag.id
                        tags.append(t)
                    pass
                picture = {
                    'id': picture_queryset.id,
                    'name': picture_queryset.name,
                    'downloads': picture_queryset.download_set.all().count(),
                    'picture_url': picture_queryset.photo_medium,
                    'picture_big_url': picture_queryset.photo_big_thumb,
                    'author': u"{0} {1}".format(user.first_name, user.last_name),
                    'author_id': user.id,
                    'author_links': links,
                    'author_thumbnail': user_profile.get_thumb(),
                    'author_photo': user_profile.get_user_picture(),
                    'likes': picture_queryset.like_set.filter().count(),
                    'liked': liked,
                    'categories': categories,
                    'tags': tags,
                    'amount': donated,
                }
                return JsonResponse({'success': "true", 'message': '', 'entity': picture})
            except Exception, e:
                return JsonResponse({'success': "false", 'message': "Wrong picture request...", "error": str(e)})


class OrganizationsView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln'])
        if check_result:
            return check_result
        else:
            #try:
            organizations = []
            organizations_queryset = Organization.objects.all()
            for organization_item in organizations_queryset:
                aggregation = Download.objects.filter(organization=organization_item.id).aggregate(price=Sum('amount'))
                donated = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
            
                aggregationUsr = Download.objects.filter(organization=organization_item.id, donator=request.GET.get('user_id')).aggregate(price=Sum('amount'))
                donatedByUsr = float(aggregationUsr.get('price', 0)) * settings.DONATED_LEFT if aggregationUsr.get('price', 0) else 0
                organization = {
                    'id': organization_item.id,
                    'name': organization_item.name,
                    'author': organization_item.author,
                    'description': organization_item.description,
                    'amount': donated,
                    'user_amount': donatedByUsr,
                }
                organizations.append(organization)
            return JsonResponse({'success': "true", 'message': '', 'entity': organizations})
            #except:
            #    return JsonResponse({'success': "false", 'message': "Some error..."})


class SearchView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page', 'param'])
        if check_result:
            return check_result
        else:
            try:
                picture_category_list = []
                picture_tag_list = []
                picture_list = Picture.objects.filter(approve_status=True, translations__name__icontains=self.param)
                category_list = Category.objects.filter(approve_status=True, translations__name__icontains=self.param)
                tag_list = Tag.objects.filter(translations__name__icontains=self.param)
                if category_list:
                    for category in category_list:
                        picture_category_list = list(chain(picture_category_list, Picture.objects.filter(approve_status=True, category=category.id)))
                if tag_list:
                    for tag in tag_list:
                        picture_tag_list = list(chain(picture_tag_list, Picture.objects.filter(approve_status=True, tag=tag.id)))
                pictures = list(chain(picture_list, picture_category_list, picture_tag_list))
                unique_results = [rows.next() for (key, rows) in groupby(pictures, key=lambda obj: obj.id)]
                if unique_results:
                    results = []
                    paginator = Paginator(unique_results, settings.PICTURES_PER_PAGE)
                    if self.page_number <= paginator.num_pages:
                        page = self.page_number
                    else:
                        page = paginator.num_pages
                    pictures_paginated = paginator.page(page)
                    for picture_item in pictures_paginated:
                        user = User.objects.get(pk=picture_item.author.id)
                        aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                        donated = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                        picture = {
                            'id': picture_item.id,
                            'name': picture_item.name,
                            'picture_url': picture_item.photo_thumb,
                            'picture_big_url': picture_item.photo_big_thumb,
                            'downloads': picture_item.download_set.all().count(),
                            'author': u"{0} {1}".format(user.first_name, user.last_name),
                            'author_id': user.id,
                            'likes': picture_item.like_set.filter().count(),
                            'amount': donated,
                        }
                        try:
                            user_profile = UserProfile.objects.get(user=user)
                            picture['author_thumbnail'] = user_profile.get_thumb()
                            picture['author_photo'] = user_profile.get_user_picture()
                        except Exception, e:
                            picture['author_thumbnail'] = None
                            picture['author_photo'] = None
                        results.append(picture)
                    return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'page_name': self.param, 'entity': results})
                else:
                    return JsonResponse({'success': "true", 'message': 'There are no results... Category results='+str(category_list.count())+'; Tags results='+str(tag_list.count())+'; Pictures results='+str(picture_list.count())})
            except:
                return JsonResponse({'success': "false", 'message': "Some error..."})

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

class DownloadAndroidView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'id', 'org_id', 'user_id', 'amount'])
        if check_result:
            return check_result
        else:
            try:
                picture = Picture.objects.filter(approve_status=True).get(pk=self.id)
                
                organization = Organization.objects.get(pk=self.org_id)
                bid = settings.CURRENCIES_COURSE
                try:
                    url = 'http://resources.finance.ua/ru/public/currency-cash.json'
                    serialized_data = urllib2.urlopen(url, timeout = 1).read()
                    data = json.loads(serialized_data)
                    orgs = data.get(u'organizations')
                    #Use PrivatBank -> LiqPay course
                    for x in orgs:
                        if x.get(u'id') == u'7oiylpmiow8iy1sma7w':
                            curses = x.get(u'currencies')
                            bid = curses.get(u'USD').get(u'ask')
                except Exception, e:
                    bid = settings.CURRENCIES_COURSE
                    print("Can't get currencies course!")
                    
                print(bid)
                # -30% Play market
                up = Download.create('%.2f' % round(((float(self.amount)*0.7)/float(bid)), 2), picture, organization, self.user_id, request.GET.get('utid_id') if request.GET.get('utid_id') else "api-android")
                up.save()
                for category in picture.category.all():
                    up.category.add(Category.objects.get(pk=int(category.id)))
                up.save()
                return HttpResponse(open(picture.photo_origin.path, "rb").read(), content_type="image/jpg")
            except:
                return JsonResponse({'success': "false", 'message': "Wrong picture request..."})

class DownloadiOSView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'id', 'org_id', 'user_uid', 'amount'])
        if check_result:
            return check_result
        else:
            try:
                picture = Picture.objects.filter(approve_status=True).get(pk=self.id)
                organization = Organization.objects.get(pk=self.org_id)

                # -30% Aplle store
                if self.amount and self.amount > 0:
                    #Pay
                    up = Download.create(float(self.amount)*0.7, picture, organization, self.user_uid, request.GET.get('utid_id') if request.GET.get('utid_id') else "pay-ios")
                else:
                    #Free
                    up = Download.create(0, picture, organization, self.user_uid, "api-ios")
                up.save()
                for category in picture.category.all():
                    up.category.add(Category.objects.get(pk=int(category.id)))
                up.save()
                return HttpResponse(open(picture.photo_origin.path, "rb").read(), content_type="image/jpg")
            except:
                return JsonResponse({'success': "false", 'message': "Wrong request..."})

class LikeView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['id', 'user'])
        if check_result:
            return check_result
        else:
            try:
                picture = Picture.objects.filter(approve_status=True).get(pk=self.id)
                try:
                    l = picture.like_set.filter(user__icontains=self.user)
                    if not l:
                        like = Like.create(self.user, picture)
                        like.save()
                        return JsonResponse({'success': "true", 'message':'Liked!'})
                    else:
                        return JsonResponse({'success': "false", 'message':'Already exist!'})
                except:
                    return JsonResponse({'success': "false", 'message': "Wrong picture in request..."})
            except:
                return JsonResponse({'success': "false", 'message': "Wrong picture request..."})


class AuthorListView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page', 'id'])
        if check_result:
            return check_result
        else:
            try:
                author_pictures = []
                links = []
                help = 0
                picture_author = User.objects.get(pk=self.id)
                picture_author_name = u"{0} {1}".format(picture_author.first_name, picture_author.last_name)
                picture_list = Picture.objects.filter(approve_status=True, author=picture_author).annotate(count=Count('download')).order_by('-count')
                paginator = Paginator(picture_list, settings.PICTURES_PER_PAGE)
                pictures_paginated = paginator.page(self.page_number if self.page_number <= paginator.num_pages else paginator.num_pages)
                
                for p in picture_list:
                    aggregation = Download.objects.filter(picture=p.id).aggregate(price=Sum('amount'))
                    donated = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                    
                    if donated:
                        help = round((float(help) + float(donated)), 2)
                        

                for picture_item in pictures_paginated:
                    aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                    donated = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                    picture = {
                        'id': picture_item.id,
                        'downloads': picture_item.download_set.all().count(),
                        'picture_url': picture_item.photo_thumb,
                        'picture_big_url': picture_item.photo_big_thumb,
                        'name': picture_item.name,
                        'author': picture_author_name,
                        'author_id': picture_author.id,
                        'likes': picture_item.like_set.filter().count(),
                        'amount': donated
                    }
                    try:
                        user_profile = UserProfile.objects.get(user=picture_author)
                        picture['author_thumbnail'] = user_profile.get_thumb()
                        picture['author_photo'] = user_profile.get_user_picture()
                    except Exception, e:
                        picture['author_thumbnail'] = None
                        picture['author_photo'] = None
                    author_pictures.append(picture)
                try:
                    user_profile = UserProfile.objects.get(user=picture_author)
                    author_thumbnail = user_profile.get_thumb()
                    author_photo = user_profile.get_user_picture()
                    for link in user_profile.links.all():
                        lnk = {}
                        lnk['link_url'] = link.link_url
                        lnk['link_type'] = link.link_type.type_tag
                        links.append(lnk)
                    
                except Exception, e:
                    author_thumbnail = None
                    author_photo = None
                
                return JsonResponse({'success': "true", 'message': '', 'page': self.page_number, 'count': paginator.num_pages, 'entity': author_pictures, 'page_name': picture_author_name, 'author_photo': author_photo, 'author_thumbnail': author_thumbnail, 'author_links': links, 'author_help': help })
            except:
                return JsonResponse({'success': "false", 'message': 'Provide vaild id'})


class TagListView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page'])
        if check_result:
            return check_result
        else:
            try:
                tags = []
                tags_list = Tag.objects.filter(approve_status=True).annotate(count=Count('download')).order_by('-count')
                paginator = Paginator(tags_list, settings.TAGS_PER_PAGE)
                if self.page_number <= paginator.num_pages:
                    page = self.page_number
                else:
                    page = paginator.num_pages
                tags_paginated = paginator.page(page)
                for tag_item in tags_paginated:
                    # pictures = Picture.objects.filter(category=tag_item.id, approve_status=True).annotate(count=Count('download')).order_by('-count').first()
                    tag = {
                        'id': tag_item.id,
                        'name': tag_item.name,
                        'downloads': tag_item.download_set.all().count(),
                    }
                    # if pictures:
                    #    tag['picture_url'] = tag_item.photo_thumb
                    tags.append(tag)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': tags})
            except:
                return JsonResponse({'success': "false", 'message': 'Some error'})


class NewestView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page'])
        if check_result:
            return check_result
        else:
            try:
                pictures_list = []
                pictures_list_queryset = Picture.objects.filter(approve_status=True).annotate(count=Count('download')).order_by('-date_approve')
                paginator = Paginator(pictures_list_queryset, settings.PICTURES_PER_PAGE)
                if self.page_number <= paginator.num_pages:
                    page = self.page_number
                else:
                    page = paginator.num_pages
                pictures_list_paginated = paginator.page(page)
                for picture_item in pictures_list_paginated:
                    picture = {
                        'id': picture_item.id,
                        'picture_url': picture_item.photo_thumb,
                        'picture_big_url': picture_item.photo_big_thumb,
                        'name': picture_item.name,
                        'downloads': picture_item.download_set.all().count(),
                        'likes': picture_item.like_set.filter().count(),
                        'date_approve': picture_item.date_approve
                    }
                    user = User.objects.get(pk=picture_item.author.id)
                    picture['author'] = "%s %s" % (user.first_name, user.last_name)
                    picture['author_id'] = user.id
                    aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                    picture['amount'] = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                    try:
                        user_profile = UserProfile.objects.get(user=user)
                        picture['author_thumbnail'] = user_profile.get_thumb()
                        picture['author_photo'] = user_profile.get_user_picture()
                    except Exception, e:
                        picture['author_thumbnail'] = None
                        picture['author_photo'] = None
                    pictures_list.append(picture)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures_list})
            except:
                return JsonResponse({'success': "false", 'message': 'Some error'})


class MostRaisedView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page'])
        if check_result:
            return check_result
        else:
            try:
                pictures_list = []
                pictures_list_queryset = Picture.objects.filter(approve_status=True).annotate(count=Count('download')).order_by('-download__amount')
                paginator = Paginator(pictures_list_queryset, settings.PICTURES_PER_PAGE)
                if self.page_number <= paginator.num_pages:
                    page = self.page_number
                else:
                    page = paginator.num_pages
                pictures_list_paginated = paginator.page(page)
                for picture_item in pictures_list_paginated:
                    picture = {
                        'id': picture_item.id,
                        'picture_url': picture_item.photo_thumb,
                        'picture_big_url': picture_item.photo_big_thumb,
                        'name': picture_item.name,
                        'downloads': picture_item.download_set.all().count(),
                        'likes': picture_item.like_set.filter().count(),
                        'date_approve': picture_item.date_approve
                    }
                    user = User.objects.get(pk=picture_item.author.id)
                    picture['author'] = "%s %s" % (user.first_name, user.last_name)
                    picture['author_id'] = user.id
                    aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                    picture['amount'] = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                    try:
                        user_profile = UserProfile.objects.get(user=user)
                        picture['author_thumbnail'] = user_profile.get_thumb()
                        picture['author_photo'] = user_profile.get_user_picture()
                    except Exception, e:
                        picture['author_thumbnail'] = None
                        picture['author_photo'] = None
                    pictures_list.append(picture)
                pictures_list = sorted(pictures_list, key=itemgetter('amount'), reverse=True)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures_list})
            except:
                return JsonResponse({'success': "false", 'message': 'Some error'})

def formatted(f): "{:.3g}".format(f) #format(f, '.2f').rstrip('0').rstrip('.')

class PhotographersView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page'])
        if check_result:
            return check_result
        else:
            try:
                photographers = []
                photographers_queryset = UserProfile.objects.all()
                paginator = Paginator(photographers_queryset, settings.PHOTOGRAPHERS_PER_PAGE)
                if self.page_number <= paginator.num_pages:
                    page = self.page_number
                else:
                    page = paginator.num_pages
                photographers_paginated = paginator.page(page)
                for photographer_item in photographers_paginated:
                    photographer = {
                        'author_id': photographer_item.user.id,
                        'author': photographer_item.user.first_name + " " + photographer_item.user.last_name,
                    }
                    user_profile = UserProfile.objects.get(user=photographer_item.user.id)
                    links = []
                    for link in user_profile.links.all():
                        lnk = {}
                        lnk['link_url'] = link.link_url
                        lnk['link_type'] = link.link_type.type_tag
                        links.append(lnk)
                    photographer['links'] = links
                    photographer['pictures'] = []
                    photographer['donated'] = 0
                    picture_list = Picture.objects.filter(approve_status=True, author=photographer_item.user.id).annotate(count=Count('download')).order_by('-count')[:settings.PHOTOS_PER_PHOTOGRAPHER]
                    for picture_item in picture_list:
                        aggregation = Download.objects.filter(picture=picture_item.id).aggregate(price=Sum('amount'))
                        donated = float(aggregation.get('price', 0)) * settings.DONATED_LEFT if aggregation.get('price', 0) else 0
                        picture = {
                            'id': picture_item.id,
                            'downloads': picture_item.download_set.all().count(),
                            'picture_url': picture_item.photo_thumb,
                            'picture_big_url': picture_item.photo_big_thumb,
                            'name': picture_item.name,
                            'likes': picture_item.like_set.filter().count(),
                            'author': photographer_item.user.first_name + " " + photographer_item.user.last_name,
                            'author_id': photographer_item.user.id,
                            'amount': donated
                        }
                        if donated:
                            photographer['donated'] = round((float(photographer['donated']) + float(donated)), 2)

                        photographer['pictures'].append(picture)
                    photographer['author_thumbnail'] = user_profile.get_thumb()
                    photographer['author_photo'] = user_profile.get_user_picture()
                    print(photographer['donated'])
                    photographer['donated'] = photographer['donated']
                    if photographer['pictures']:
                        photographers.append(photographer)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': photographers})
            except:
                return JsonResponse({'success': "false", 'message': 'Some error'})
