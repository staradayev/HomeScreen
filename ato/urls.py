from django.conf.urls import patterns, url
from django.contrib import auth

from ato import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView, name='index'),
    url(r'^ua/$', views.IndexUAView, name='index'),
    url(r'^en/$', views.IndexENView, name='index'),
    url(r'^ppen/$', views.PPEView, name='ppEnglish'),
    url(r'^ppua/$', views.PPUView, name='ppUkrainian'),
    url(r'^social/$', views.SocialView, name='social'),
)
