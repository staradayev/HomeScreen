from django.conf.urls import patterns, url
from django.contrib import auth

from care import views

urlpatterns = patterns('',
    url(r'^$', views.DetailView, name='detail'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'care/login.html', 'extra_context': {'next':'/care/detail'}}),
    url(r'^logged/', views.logged, name='logged'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^detail/', views.DetailView, name='detail'),
    url(r'^loggedout/', views.loggedout, name='loggedout'),
    url(r'^myinfo/', views.InfoView, name='myinfo'),
    #Temp for debug
    url(r'^addupload/(?P<picture_id>\d+)/$', views.AddUploadView, name='addupload'),
    url(r'^addlike/(?P<picture_id>\d+)/$', views.AddLikeView, name='addlike'),
    url(r'^like/(?P<picture_id>\d+)/$', views.AddLikePhotographerView, name='like'),
    
    #end Temp for debug
    url(r'^upload/', views.UploadView, name='upload'),
    url(r'^addcategory/', views.AddCategoryView, name='addcat'),
    url(r'^addtag/', views.AddTagView, name='addtag'),
    url(r'^addlink/', views.AddLinkView, name='addlink'),
    url(r'^edit/(?P<picture_id>\d+)/$', views.EditView, name='edit'),
    url(r'^uploadpicture/$', views.UploadPictureView, name = 'jfu_upload' ),
    # You may optionally define a delete url as well
    url(r'^delete/(?P<pk>\d+)$', views.upload_delete, name = 'jfu_delete' ),
    url(r'^addthumb/', views.upload_thumb, name='add_thumb'),
    url(r'^adddescription/', views.upload_description, name='add_descr'),
    url(r'^getcategory/', views.GetCategoryView, name='get_cat'),
    url(r'^gettag/', views.GetTagView, name='get_tag'),
    url(r'^getpictures/', views.get_picture_list, name='get_pics'),
    url(r'^adduserphoto/$', views.upload_user_photo, name = 'upload_user_photo' ),
    url(r'^adduserthumb/$', views.upload_user_thumb, name = 'upload_user_thumb' ),
    
    url(r'^rotatephoto/$', views.rotate_photo, name = 'rotate_photo' ),
    
)