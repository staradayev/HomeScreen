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
)