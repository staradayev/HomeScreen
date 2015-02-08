from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns(
    '',
    url(r'^categories/$', views.CategoryListView.as_view()),
    url(r'^popular/$', views.PopularListView.as_view()),
    url(r'^catpictures/$', views.PictureByCategoryListView.as_view()),
    url(r'^picture/$', views.PictureView.as_view()),
    url(r'^organizations/$', views.OrganizationsView.as_view()),
    url(r'^search/$', views.SearchView.as_view()),
    url(r'^download/$', views.DownloadView.as_view()),
    url(r'^author/$', views.AuthorListView.as_view()),
    url(r'^tags/$', views.TagListView.as_view()),
    url(r'^newest/$', views.NewestView.as_view()),
    url(r'^mostraised/$', views.MostRaisedView.as_view()),
    url(r'^photographers/$', views.PhotographersView.as_view()),
)
