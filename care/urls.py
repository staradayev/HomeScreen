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
    url(r'^upload/', views.UploadView, name='upload'),
)