from django.conf.urls import patterns, url
from django.contrib import auth

from ato import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView, name='index'),
)