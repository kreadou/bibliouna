from django.conf.urls import url
from django.urls import re_path, path
from publication import views

app_name="publication"
urlpatterns = [
	path('traitement/', views.traitement, name='traitement'),
	url(r'publication_detail/(?P<pk>[0-9]+)/$', views.publication_detail, name='publication_detail'),

	url(r'ouvragre_detail/(?P<pk>[0-9]+)/$', views.ouvrage_detail, name='ouvrage_detail'),
	url(r'article_detail/(?P<pk>[0-9]+)/$', views.article_detail, name='article_detail'),

	path('telechargement/', views.telechargement, name='telechargement'),


]


