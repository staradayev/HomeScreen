from django.conf.urls import patterns, url, include
from django.contrib import auth
from api import views

urlpatterns = patterns('',
	url(r'^categories/$', views.category_list),
	url(r'^popular/$', views.popular_list),
	url(r'^catpictures/$', views.picture_by_cat_list),
	url(r'^picture/$', views.picture),
	url(r'^organizations/$', views.organizations),
	url(r'^search/$', views.search),
	url(r'^download/$', views.download),
)