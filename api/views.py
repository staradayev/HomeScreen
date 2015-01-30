from django.views.generic.base import View
from django.http import JsonResponse
from care.models import Category, Download, Picture, Organization, Tag
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import translation
from itertools import chain, groupby
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from validate_email import validate_email
from django.conf import settings


class BaseMixin(View):
    http_method_names = ['get']

    def http_method_not_allowed(self, request):
        return JsonResponse({'success': "false", 'message': 'Only GET allowed'})

    def dispatch(self, request):
        self.language = request.GET.get('ln')
        self.page_number = request.GET.get('page')
        self.id = request.GET.get('id')
        self.user_id = request.GET.get('user_id')
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
                if not validate_email(request.GET.get(param), verify=True):
                    return JsonResponse({'success': "false", 'message': "Please provide valid" + param})


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
                    'name': picture_item.name,
                    'downloads': picture_item.download_set.all().count(),
                }
                user = User.objects.get(pk=picture_item.author.id)
                picture['author'] = "%s %s" % (user.first_name, user.last_name)
                picture['author_id'] = user.id
                donated = Download.objects.filter(picture=picture_item.id).aggregate(Sum('amount'))
                picture['amount'] = str(int(donated['amount__sum']) * settings.DONATED_LEFT) if donated['amount__sum'] else 0
                pictures.append(picture)
            return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures})


class PictureByCategoryListView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page', 'id'])
        if check_result:
            return check_result
        else:
            pictures_queryset = Picture.objects.filter(approve_status=True, category=self.id).annotate(count=Count('download')).order_by('-count')
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
                        'name': picture_item.name,
                        'downloads': picture_item.download_set.all().count(),
                    }
                    user = User.objects.get(pk=picture_item.author.id)
                    picture['author'] = "%s %s" % (user.first_name, user.last_name)
                    picture['author_id'] = user.id
                    donated = Download.objects.filter(picture=picture_item.id).aggregate(Sum('amount'))
                    picture['amount'] = str(int(donated['amount__sum']) * settings.DONATED_LEFT) if donated['amount__sum'] else 0
                    pictures.append(picture)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures})
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
                donated = Download.objects.filter(picture=picture_queryset.id).aggregate(Sum('amount'))
                picture = {
                    'id': picture_queryset.id,
                    'name': picture_queryset.name,
                    'downloads': picture_queryset.download_set.all().count(),
                    'picture_url': picture_queryset.photo_medium,
                    'author': "{0} {1}".format(user.first_name, user.last_name),
                    'author_id': user.id,
                    'amount': str(int(donated['amount__sum']) * settings.DONATED_LEFT) if donated['amount__sum'] else 0
                }
                return JsonResponse({'success': "true", 'message': '', 'entity': picture})
            except:
                return JsonResponse({'success': "false", 'message': "Wrong picture request..."})


class OrganizationsView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'id'])
        if check_result:
            return check_result
        else:
            try:
                organizations = []
                organizations_queryset = Organization.objects.all()
                for organization_item in organizations_queryset:
                    donated = Download.objects.filter(organization=organization_item.id).aggregate(Sum('amount'))
                    donatedByUsr = Download.objects.filter(organization=organization_item.id, donator=request.GET.get('user_id')).aggregate(Sum('amount'))
                    organization = {
                        'id': organization_item.id,
                        'name': organization_item.name,
                        'author': organization_item.author,
                        'description': organization_item.description,
                        'amount': str(int(donated['amount__sum']) * settings.DONATED_LEFT) if donated['amount__sum'] else 0,
                        'user_amount': str(int(donatedByUsr['amount__sum']) * settings.DONATED_LEFT) if donatedByUsr['amount__sum'] else 0
                    }
                    organizations.append(organization)
                return JsonResponse({'success': "true", 'message': '', 'entity': organizations})
            except:
                return JsonResponse({'success': "false", 'message': "Some error..."})


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
                tag_list = Tag.objects.filter(approve_status=True, translations__name__icontains=self.param)
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
                        donated = Download.objects.filter(picture=picture_item.id).aggregate(Sum('amount'))
                        picture = {
                            'id': picture_item.id,
                            'name': picture_item.name,
                            'picture_url': picture_item.photo_thumb,
                            'downloads': picture_item.download_set.all().count(),
                            'author': "{0} {1}".format(user.first_name, user.last_name),
                            'author_id': user.id,
                            'amount': str(int(donated['amount__sum']) * settings.DONATED_LEFT) if donated['amount__sum'] else 0
                        }
                        results.append(picture)
                    return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'page_name': page, 'entity': results})
                else:
                    return JsonResponse({'success': "true", 'message': 'There are no results...'})
            except:
                return JsonResponse({'success': "false", 'message': "Some error..."})


class DownloadView(BaseMixin):
    def get(self, request):
        check_result = self.check_params(request, params_list=['ln', 'page', 'id', 'org_id', 'user_id', 'amount'])
        if check_result:
            return check_result
        else:
            try:
                picture = Picture.objects.filter(approve_status=True).get(pk=self.id)
                try:
                    organization = Organization.objects.get(pk=self.org_id)
                    up = Download.create(self.amount, picture, organization, self.user_id, "api-development")
                    up.save()
                    for category in picture.category.all():
                        up.category.add(Category.objects.get(pk=int(category.id)))
                    up.save()
                    return HttpResponse(open(picture.photo_origin.path, "rb").read(), content_type="image/jpg")
                except:
                    return JsonResponse({'success': "false", 'message': "Wrong organization in request..."})
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
                picture_author = User.objects.get(pk=self.id)
                picture_author_name = "{0} {1}".format(picture_author.first_name, picture_author.last_name)
                picture_list = Picture.objects.filter(approve_status=True, author=picture_author).annotate(count=Count('download')).order_by('-count')
                paginator = Paginator(picture_list, settings.PICTURES_PER_PAGE)
                pictures_paginated = paginator.page(self.page_number if self.page_number <= paginator.num_pages else paginator.num_pages)
                for picture_item in pictures_paginated:
                    donated = Download.objects.filter(picture=picture_item.id).aggregate(Sum('amount'))
                    picture = {
                        'id': picture_item.id,
                        'downloads': picture_item.download_set.all().count(),
                        'picture_url': picture_item.photo_thumb,
                        'name': picture_item.name,
                        'author': picture_author_name,
                        'author_id': picture_author.id,
                        'amount': str(int(donated['amount__sum']) * settings.DONATED_LEFT) if donated['amount__sum'] else 0
                    }
                    author_pictures.append(picture)
                return JsonResponse({'success': "true", 'message': '', 'page': self.page_number, 'count': paginator.num_pages, 'entity': author_pictures, 'page_name': picture_author_name})
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
                    pictures = Picture.objects.filter(category=tag_item.id, approve_status=True).annotate(count=Count('download')).order_by('-count').first()
                    tag = {
                        'id': tag_item.id,
                        'name': tag_item.name,
                        'downloads': tag_item.download_set.all().count(),
                    }
                    if pictures:
                        tag['picture_url'] = tag_item.photo_thumb
                    tags.append(tag)
                return JsonResponse({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': tags})
            except:
                return JsonResponse({'success': "false", 'message': 'Some error'})
