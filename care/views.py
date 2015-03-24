from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from care.models import Picture, PictureTranslation, Category, CategoryTranslation, Tag, TagTranslation, LinkType, Link, UserProfile, Download, Organization, Like
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render
import datetime
from django.utils import translation
import json as simplejson
from django.db.models import Q, Count
from django.utils.translation import ugettext as _
from care.forms import UserInfoForm, UploadPictureForm, EditPictureForm
import urllib
from unidecode import unidecode
from django.core.urlresolvers import reverse
import os
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse, UploadResponseError
from django.conf import settings
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.utils import formats
from additional import UploadFile
from liqpay import LiqPay
from django.shortcuts import render_to_response
import re
from uuid import uuid4

def custom_404(request):
    return render_to_response('care/404.html')


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

    p_author = User.objects.get(username=request.user.username)
    picture_list = Picture.objects.filter(author=p_author, complete_status=True).order_by('-date_pub').all()
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
    user_pic = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserInfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = User.objects.get(username=request.user.username)
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
        user = User.objects.get(username=request.user.username)
        form = UserInfoForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
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

        try:
            pic_u = UserProfile.objects.get(user=user, user_picture='', user_thumbnail='')
            print(pic_u.original_picture)
            print(pic_u.user_picture)
            print(pic_u.user_thumbnail)
            if(pic_u.original_picture):
                pic_complete = {}
                pic_complete['url'] =  settings.MEDIA_URL + pic_u.original_picture
                print('found uncompleted picture')
            else:
               pic_complete = None 
        except:
            pic_complete = None
            print('No uncompleted pictures')

    try:
        user = User.objects.get(username=request.user.username)
        user_p = UserProfile.objects.get(user=user)
        user_pic = settings.MEDIA_URL + user_p.user_picture
        print ("!="+user_pic)
        if '' == user_p.user_picture:
            user_pic = settings.STATIC_URL + 'img/default/ato-user.png'
    except:
        user_pic = settings.STATIC_URL + 'img/default/ato-user.png'

    return render(request, 'care/myinfo.html', {'form': form, 'name_empty': name_empty, 'link_types': link_types, 'user_links': user_links, 'user_picture': user_pic, 'user_p':user_p, 'unfinished':pic_complete})


@login_required()
def UploadView(request):
    if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
        return HttpResponseRedirect('/care/myinfo')

    limit_detected = False
    p_author = User.objects.get(username=request.user.username)
    date = datetime.date
    today_min = datetime.datetime.combine(date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(date.today(), datetime.time.max)
    pics = Picture.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
    if pics.count() > 24:
        limit_detected = True

    try:
        pic_u = Picture.objects.filter(complete_status=False, author=p_author).first()
        pic_complete = {}
        pic_complete['url'] = pic_u.photo_origin.url
        pic_complete['id'] = pic_u.pk
        pic_complete['deleteUrl'] = reverse('care:jfu_delete', kwargs={'pk': pic_u.pk})
        print('found uncompleted picture')
    except:
        pic_complete = None
        print('No uncompleted pictures')

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
            'tags': tags})

    return render(request, 'care/upload.html', {'form': form, 'limit_detected': limit_detected, 'not_completed': pic_complete})


@login_required()
def EditView(request, picture_id):
    if hasattr(request.user, 'first_name') and not request.user.last_name or not request.user.first_name:
        return HttpResponseRedirect('/care/myinfo')
    selected_image = None
    limit_detected = False
    p_author = User.objects.get(username=request.user.username)
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

        # if a GET (or any other method) we'll create a blank form
        else:
            categories = Category.objects.filter(Q(approve_status=True) | Q(author=p_author))
            tags = Tag.objects.filter(Q(approve_status=True) | Q(author=p_author))
            CATEGORY_CHOICES = [[x.id, x.name] for x in categories]
            TAG_CHOICES = [[x.id, x.name] for x in tags]
            form = EditPictureForm(CATEGORY_CHOICES, TAG_CHOICES, initial={
                'categories': categories,
                'tags': tags,
                'name': selected_image.name})

        pic_complete = {}
        pic_complete['url'] = selected_image.photo_origin.url
        pic_complete['id'] = selected_image.pk
        pic_complete['deleteUrl'] = reverse('care:jfu_delete', kwargs={'pk': selected_image.pk})

    return render(request, 'care/edit.html', {'form': form, 'limit_detected': limit_detected, 'img': selected_image, 'image': pic_complete})


@login_required
def AddCategoryView(request):
    data = simplejson.loads(request.body)

    if data is not None:
        category_send = urllib.url2pathname(unidecode(data["category_name"]))
        print category_send
        p_author = User.objects.get(username=request.user.username)
        date = datetime.date
        today_min = datetime.datetime.combine(date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(date.today(), datetime.time.max)
        categories = Category.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
        if categories.count() > 14:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"You were added maximum count of categories per today. Try tomorrow!")}), content_type="application/json")
        elif not category_send:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There are no category name presented!")}), content_type="application/json")
        elif len(category_send) < 3:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Category name too short ( minimum 3 symbols )")}), content_type="application/json")
        elif len(category_send) > 75:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Category name too long ( maximum 75 symbols )")}), content_type="application/json")
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

            # , "data" : dataReturn
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@login_required
def AddTagView(request):
    data = simplejson.loads(request.body)

    if data is not None:
        tag_send = urllib.url2pathname(unidecode(data["tag_name"]))
        print tag_send
        p_author = User.objects.get(username=request.user.username)
        date = datetime.date
        today_min = datetime.datetime.combine(date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(date.today(), datetime.time.max)
        tags = Tag.objects.filter(author=p_author, date_pub__range=(today_min, today_max))
        if tags.count() > 14:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"You were added maximum count of tags per today. Try tomorrow!")}), content_type="application/json")
        elif not tag_send:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There are no tag name presented!")}), content_type="application/json")
        elif len(tag_send) < 3:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Tag name too short ( minimum 3 symbols )")}), content_type="application/json")
        elif len(tag_send) > 75:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Tag name too long ( maximum 75 symbols )")}), content_type="application/json")
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

            # , "data" : dataReturn
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@login_required
def AddLinkView(request):
    data = simplejson.loads(request.body)

    if data is not None:
        link_type = data["link_type"]
        link_url = data["link_url"]
        links = UserProfile.objects.filter(user=request.user)
        if links.count() > 9:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"You have maximum limit of links (10 links for user)")}), content_type="application/json")
        elif not link_type:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Choose link type, please!")}), content_type="application/json")
        elif not link_url:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There are no url name presented!")}), content_type="application/json")
        elif len(link_url) < 5:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Url too short!")}), content_type="application/json")
        elif len(link_url) > 199:
            return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Url too long!")}), content_type="application/json")
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

                # , "data" : dataReturn
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            except:
                return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")

    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


# Development section
@login_required()
def AddUploadView(request, picture_id):
    picture = Picture.objects.get(pk=picture_id)
    p_author = User.objects.get(username=request.user.username)
    organization = Organization.objects.get(pk=1)
    up = Download.create("0.99", picture, organization, p_author.email, "care-development")
    up.save()
    for cat in picture.category.all():
        up.category.add(Category.objects.get(pk=int(cat.id)))
    up.save()

    return HttpResponse("Thank you, upload tracked!")

@login_required()
def AddLikeView(request, picture_id):
    picture = Picture.objects.get(pk=picture_id)
    p_author = User.objects.get(username=request.user.username)
    l = picture.like_set.filter(user__icontains=p_author.email)
    if not l:
        like = Like.create(p_author.email, picture)
        like.save()

        return HttpResponse("Thank you, like tracked!")
    else:
        return HttpResponse("Already tracked tracked!")
    

# End of developing section
@csrf_exempt
def upload_thumb(request):
    data = simplejson.loads(request.body)
    pic = {}
    if data is not None:
        try:
            pic = Picture.objects.get(pk=data["pic_id"])
            print("Thumbnail:")
            print(pic.photo_origin.path)
            print(settings.MEDIA_ROOT + pic.photo_medium)
            print(settings.MEDIA_ROOT + pic.photo_thumb)
            im = Image.open(pic.photo_origin.path)
            w, h = im.size
            # 'try crop and save'
            im.crop((int(w*data["left"]), int(h*data["top"]), int(w*data["right"]), int(h*data["bottom"]))).save(settings.MEDIA_ROOT + pic.photo_thumb)
            # 'try open and resize'
            img = Image.open(settings.MEDIA_ROOT + pic.photo_thumb).resize((240, 240))
            # 'try save'
            img.save(settings.MEDIA_ROOT + pic.photo_thumb)

            im2 = Image.open(pic.photo_origin.path)
            # 'try crop and save'
            im2.crop((int(w*data["left"]), int(h*data["top"]), int(w*data["right"]), int(h*data["bottom"]))).save(settings.MEDIA_ROOT + pic.photo_big_thumb)

            imgBig = Image.open(settings.MEDIA_ROOT + pic.photo_big_thumb).resize((600, 600))
            imgBig.save(settings.MEDIA_ROOT + pic.photo_big_thumb)
            # settings.MEDIA_ROOT + pic.photo_thumb
            # 'saved'
            response_data = {}
            response_data['success'] = 'true'
            response_data['id'] = pic.id

            # , "data" : dataReturn
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        except:
            return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong picture request..."}), content_type="application/json")
    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@login_required()
def upload_description(request):
    data = simplejson.loads(request.body)
    selected_image = None
    if data is not None:
        try:
            p_author = User.objects.get(username=request.user.username)
            if not data["pic_id"]:
                return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Provide picture...")}), content_type="application/json")

            try:
                selected_image = Picture.objects.get(Q(pk=data["pic_id"]), Q(approve_status=False), Q(author=p_author))
            except (KeyError, Picture.DoesNotExist):
                return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Picture is wrong")}), content_type="application/json")

            name = ""
            if not data["pic_name"]:
                return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Picture name is required")}), content_type="application/json")
            elif len(data["pic_name"]) < 2:
                return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Picture name too short!")}), content_type="application/json")
            elif len(data["pic_name"]) > 99:
                return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"Picture name too long!")}), content_type="application/json")
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
                selected_image.category.clear()
                for cat in data["pic_cats"]:
                    selected_image.category.add(Category.objects.get(pk=int(cat)))
            if data["pic_tags"]:
                selected_image.tag.clear()
                for t in data["pic_tags"]:
                    selected_image.tag.add(Tag.objects.get(pk=int(t)))

            if data["pic_cats"] or data["pic_tags"]:
                selected_image.save()

            selected_image.complete_status = True
            selected_image.save()

            return HttpResponse(simplejson.dumps({'success': "true", 'message': "Saved success!"}), content_type="application/json")
        except:
            return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong picture request..."}), content_type="application/json")
    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


@require_POST
def UploadPictureView(request):

    # The assumption here is that jQuery File Upload
    # has been configured to send files one at a time.
    # If multiple files can be uploaded simulatenously,
    # 'file' may be a list of files.
    try:
        file = upload_receive(request)

        p_author = User.objects.get(username=request.user.username)

        image = file

        if not image:
            return UploadResponseError(request, {
                "error": (_(u"No image!")),
                "url": "",
                "thumbnail_url": "",
                "delete_url": "",
                "delete_type": "DELETE",
                "name": '',
                "size": ''
            })
        else:
            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                return UploadResponseError(request, {
                    "error": (_(u'Please use a JPEG or PNG image.')),
                    "url": "",
                    "thumbnail_url": "",
                    "delete_url": "",
                    "delete_type": "DELETE",
                    "name": '',
                    "size": ''
                })

            # validate file size
            if len(image) > (10 * 1024 * 1024):
                return UploadResponseError(request, {
                    "error": (_(u'Image file too large')),
                    "url": "",
                    "thumbnail_url": "",
                    "delete_url": "",
                    "delete_type": "DELETE",
                    "name": '',
                    "size": ''
                })
            from django.core.files.images import get_image_dimensions
            w, h = get_image_dimensions(image)
            print("Dimensions w="+str(w)+"; h="+str(h)+";")
            # validate dimensions
            mwidth = 1920
            mheight = 1080
            if (w >= h and (w < mwidth and h < mheight)) or (w < h and (h < mwidth and w < mheight)):
                return UploadResponseError(request, {
                    "error": (_(u"Too low image size, please use bigger!")),
                    "url": "",
                    "thumbnail_url": "",
                    "delete_url": "",
                    "delete_type": "DELETE",
                    "name": '',
                    "size": ''
                })
            # portaint or landscape max size check
            if (w >= h and (w > mwidth*8 and h > mheight*8)) or (w < h and (h > mwidth*8 and w > mheight*8)):
                return UploadResponseError(request, {
                    "error": (_(u"Too big image size! Please use smaller.")),
                    "url": "",
                    "thumbnail_url": "",
                    "delete_url": "",
                    "delete_type": "DELETE",
                    "name": '',
                    "size": ''
                })

        instance = Picture.create(file, p_author)
        instance.save()

        basename = os.path.basename(instance.photo_origin.path)

        file_dict = {
            'name': basename,
            'size': file.size,
            'url': instance.photo_origin.url,
            'thumbnailUrl': instance.photo_origin.url,
            'deleteUrl': reverse('care:jfu_delete', kwargs={'pk': instance.pk}),
            'deleteType': 'POST',
            'id': instance.id
        }

        print("Uploaded:")
        print(instance.photo_origin.path)
        print(settings.MEDIA_ROOT + instance.photo_medium)
        print(settings.MEDIA_ROOT + instance.photo_thumb)

        return UploadResponse(request, file_dict)
    except Exception, e:
        return UploadResponseError(request, {
                "error": (_(u"No image!"))+str(e),
                "url": "",
                "thumbnail_url": "",
                "delete_url": "",
                "delete_type": "DELETE",
                "name": '',
                "size": ''
            })


@require_POST
def upload_delete(request, pk):
    success = True
    try:
        instance = Picture.objects.get(pk=pk)
        p_author = User.objects.get(username=request.user.username)
        if instance.author.id == p_author.id and instance.approve_status == False:
            os.unlink(instance.photo_origin.path)
            instance.delete()
            success = {'success': "true", 'message': ''}
        else:
            success = {'success': "false", 'message': (_("This photo can't be deleted"))}
    except Picture.DoesNotExist:
        success = {'success': "false", 'message': (_("Can't delete photo"))}

    return JFUResponse(request, success)


def GetCategoryView(request):
    if request.method == 'GET':
        if not request.GET.get('query'):
            return HttpResponse(simplejson.dumps({'success': "false", 'message': 'Provide query'}), content_type="application/json")

        p_author = User.objects.get(username=request.user.username)
        categories = []
        cats = Category.objects.filter(Q(approve_status=True) | Q(author=p_author) | Q(translations__name__icontains=request.GET.get('query'))).annotate(count=Count('download')).order_by('-count')

        # try:
        if cats:
            for cat in cats:
                category = {}
                category['id'] = cat.id
                category['name'] = cat.name
                # pics = Picture.objects.filter(category=cat.id).annotate(count = Count('download')).order_by('-count').first().photo_thumb

                # category['picture_url'] = pics

                categories.append(category)

        json_posts = simplejson.dumps({'success': "true", 'message': '', 'entity': categories})
        response = HttpResponse(json_posts, content_type="application/json")
        # except:
        # response = HttpResponse(simplejson.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
    else:
        response = HttpResponse(simplejson.dumps({'success': "false", 'message': 'Only GET allowed'}), content_type="application/json")

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def GetTagView(request):
    if request.method == 'GET':
        if not request.GET.get('query'):
            return HttpResponse(simplejson.dumps({'success': "false", 'message': 'Provide query'}), content_type="application/json")

        p_author = User.objects.get(username=request.user.username)
        res_tags = []
        tags = Tag.objects.filter(Q(approve_status=True) | Q(author=p_author) | Q(translations__name__icontains=request.GET.get('query')))

        # try:
        if tags:
            for t in tags:
                tag = {}
                tag['id'] = t.id
                tag['name'] = t.name

                res_tags.append(tag)

        json_posts = simplejson.dumps({'success': "true", 'message': '', 'entity': res_tags})
        response = HttpResponse(json_posts, content_type="application/json")
        # except:
        # response = HttpResponse(simplejson.dumps({'success':"false", 'message':"Some error..."}), content_type="application/json")
    else:
        response = HttpResponse(simplejson.dumps({'success': "false", 'message': 'Only GET allowed'}), content_type="application/json")

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def get_picture_list(request):
    if request.method == 'GET':

        pictures = []

        p_author = User.objects.get(username=request.user.username)
        picture_list = Picture.objects.filter(author=p_author, complete_status=True).order_by('-date_pub').all()
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
                picture = {}
                picture['id'] = pic.id
                picture['name'] = pic.name
                picture['downloads'] = pic.download_set.filter().count()
                picture['likes'] = pic.like_set.filter().count()
                if pic.like_set.filter(user=p_author.email).count() > 0:
                    picture['liked'] = 'true'
                else:
                    picture['liked'] = 'false'
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
                        category = {}
                        category['id'] = cat.id
                        category['name'] = cat.name
                        picture['cats'].append(category)

                if pic.tag.all():
                    picture['tags'] = []
                    p_tags = pic.tag.all()
                    for tag in p_tags:
                        t = {}
                        t['id'] = tag.id
                        t['name'] = tag.name
                        picture['tags'].append(t)

                if pic.download_count():
                    picture['downloads'] = pic.download_count()

                pictures.append(picture)

            json_posts = simplejson.dumps({'success': "true", 'message': '', 'page': page, 'count': paginator.num_pages, 'entity': pictures})
            response = HttpResponse(json_posts, content_type="application/json")
        except:
            response = HttpResponse(simplejson.dumps({'success': "false", 'message': "Some error..."}), content_type="application/json")
    else:
        response = HttpResponse(simplejson.dumps({'success': "false", 'message': 'Only GET allowed'}), content_type="application/json")

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@csrf_exempt
@login_required
def upload_user_photo(request):

    if request.method == 'POST':
        uploadfile = UploadFile(request=request, key='files', location='upload')
        return uploadfile.upload(request.user.id)


@login_required
def rotate_photo(request):
    data = simplejson.loads(request.body)
    pic = {}
    if data is not None:
        try:
            pic = Picture.objects.get(pk=data["pic_id"])
            print("Uploaded:")
            print(pic.photo_origin.path)
            print(settings.MEDIA_ROOT + pic.photo_medium)
            print(settings.MEDIA_ROOT + pic.photo_thumb)

            angle = 270
            if data["angle"] == "left":
                angle = 90
            else:
                angle = 270
            im = Image.open(pic.photo_origin.path)
            w, h = im.size
            print("rotate origin: " + pic.photo_origin.path)
            # rotating it by built in PIL command
            rotated_origin = im.rotate(angle)
            # saving rotated image instead of original. Overwriting is on.
            rotated_origin.save(pic.photo_origin.path, overwrite=True)
            print("rotate medium: " + settings.MEDIA_ROOT+pic.photo_medium)
            # rotating it by built in PIL command
            rotated_medium = Image.open(settings.MEDIA_ROOT + pic.photo_medium).rotate(angle)
            # saving rotated image instead of original. Overwriting is on.
            rotated_medium.save(settings.MEDIA_ROOT+pic.photo_medium, overwrite=True)
            print("rotate thumb: " + settings.MEDIA_ROOT+pic.photo_thumb)
            # rotating it by built in PIL command
            rotated_thumb = Image.open(settings.MEDIA_ROOT + pic.photo_thumb).rotate(angle)
            # saving rotated image instead of original. Overwriting is on.
            rotated_thumb.save(settings.MEDIA_ROOT+pic.photo_thumb, overwrite=True)
            print("All done!")
            # settings.MEDIA_ROOT + pic.photo_thumb
            # 'saved'
            response_data = {}
            response_data['success'] = 'true'
            response_data['id'] = pic.id

            # , "data" : dataReturn
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        except:
            return HttpResponse(simplejson.dumps({'success':"false", 'message':"Wrong picture request..."}), content_type="application/json")
    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")

@login_required
def AddLikePhotographerView(request, picture_id):
    try:
        picture = Picture.objects.get(pk=picture_id)
        p_author = User.objects.get(username=request.user.username)
        l = picture.like_set.filter(user__icontains=p_author.email)
        if not l:
            like = Like.create(p_author.email, picture)
            like.save()

            response_data = {}
            response_data['success'] = 'true'
            response_data['likes'] = picture.like_set.filter().count()

            # , "data" : dataReturn
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse("Already tracked tracked!")
    except Exception, e:
        return HttpResponse(simplejson.dumps({'success':"false", 'message':"Wrong request..."}), content_type="application/json")
    

@csrf_exempt
def upload_user_thumb(request):
    data = simplejson.loads(request.body)
    pic = {}
    if data is not None:
        try:
            user = User.objects.get(username=request.user.username)
            user_p = UserProfile.objects.get(user=user)
            pic = user_p.original_picture
            print("UserProfile photo original:" + pic)

            ext = user_p.original_picture.split('.')[-1]
            # get filename
            
            m = re.search('(^.*/)(\w{10,50}\.\w{2,3}$)', pic)
            filepath = m.group(1)
            print("FilePath: "+filepath)
            im = Image.open(settings.MEDIA_ROOT + pic)
            w, h = im.size
            # 'try crop and save'
            filename2 = '{}.{}'.format(uuid4().hex, ext)
            user_p.user_picture = filepath + filename2
            im.crop((int(w*data["left"]), int(h*data["top"]), int(w*data["right"]), int(h*data["bottom"]))).resize((400, 400)).save(settings.MEDIA_ROOT + user_p.user_picture)

            # 'try open and resize'
            filename1 = '{}.{}'.format(uuid4().hex, ext)
            img = Image.open(settings.MEDIA_ROOT + user_p.user_picture).resize((50, 50))
            user_p.user_thumbnail = filepath + filename1
            user_p.save()
            # 'try save'
            img.save(settings.MEDIA_ROOT + user_p.user_thumbnail)
            
            
            # settings.MEDIA_ROOT + pic.photo_thumb
            # 'saved'
            response_data = {}
            response_data['success'] = 'true'
            response_data['pic_url'] = str('http://'+request.META['HTTP_HOST']+settings.MEDIA_URL + user_p.user_picture)


            # , "data" : dataReturn
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        except:
            return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong picture request..."}), content_type="application/json")
    else:
        # , "message" : "Invalid data received by server"
        return HttpResponse(simplejson.dumps({'success': "False", 'message': _(u"There is an error! Please contact us, if you know why?")}), content_type="application/json")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def FreeLoadView(request, picture_id, org_id):
    try:
        picture = Picture.objects.get(pk=picture_id)
        #p_author = User.objects.get(username=request.user.username)
        organization = Organization.objects.get(pk=org_id)
        up = Download.create(0, picture, organization, get_client_ip(request), "free")
        up.save()
        for cat in picture.category.all():
            up.category.add(Category.objects.get(pk=int(cat.id)))
        up.save()

        return HttpResponse(open(picture.photo_origin.path, "rb").read(), content_type="image/jpg")
    except Exception, e:
        return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong request..."}), content_type="application/json")

def FreeLoadView(request, picture_id, org_id):
    try:
        picture = Picture.objects.get(pk=picture_id)
        #p_author = User.objects.get(username=request.user.username)
        organization = Organization.objects.get(pk=org_id)
        up = Download.create(0, picture, organization, get_client_ip(request), "free")
        up.save()
        for cat in picture.category.all():
            up.category.add(Category.objects.get(pk=int(cat.id)))
        up.save()

        return HttpResponse(open(picture.photo_origin.path, "rb").read(), content_type="image/jpg")
    except Exception, e:
        return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong request..."}), content_type="application/json")


def PayLoadView(request, picture_id, org_id):
    #try:
    picture = Picture.objects.get(pk=picture_id)
    #p_author = User.objects.get(username=request.user.username)
    organization = Organization.objects.get(pk=org_id)
    
    lang = "ru"
    if translation.get_language() == "en":
        lang = "en"

    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        user_id = user.email
    else:
        user_id = get_client_ip(request)
    order = Download.create(0, picture, organization, user_id, "web-liqpay")
    order.save()

    liqpay = LiqPay(settings.LIQPAY_PUBLIC, settings.LIQPAY_PRIVAT)
    html_f = liqpay.cnb_form({
        "version" : "3",
        "amount" : "1",
        "currency" : "USD",
        "description" : "Donate for "+organization.name,
        "order_id" : order.id,
        "result_url" : "http://dev.ato.care/care/donload/"+picture_id+"/"+org_id+"/"+str(order.id),
        "language" : lang,
        "sandbox": 1,
    })

    return HttpResponse(simplejson.dumps({'success': "true", 'message': "", 'form':html_f}), content_type="application/json")
    #except Exception, e:
    #    return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong request..."}), content_type="application/json")

def DonLoadView(request, picture_id, org_id, ord_id):
    try:
        order = Download.objects.get(pk=ord_id, picture=picture_id, organization=org_id)
        if(order.amount == 0):
            order.amount = 0.98
            order.save()

            picture = Picture.objects.get(pk=picture_id)
            return HttpResponse(open(picture.photo_origin.path, "rb").read(), content_type="image/jpg")
        else:
            return HttpResponse(simplejson.dumps({'success': "false", 'message': "Dublicate request"}), content_type="application/json")
    except Exception, e:
        return HttpResponse(simplejson.dumps({'success': "false", 'message': "Wrong request..."}), content_type="application/json")

