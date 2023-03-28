from django.conf.urls import url
from django.urls import re_path, path
from . import views

app_name="actualite"
urlpatterns = [
	url(r'evenement_lister/$', views.evenement_lister, name='evenement_lister'), 
	url(r'evenement_creer/$', views.evenement_creer, name='evenement_creer'),
	url(r'evenement_modifier/(?P<pk>[0-9]+)/$', views.evenement_modifier, name='evenement_modifier'),
	url(r'evenement_visualiser/(?P<pk>[0-9]+)/$', views.evenement_visualiser, name='evenement_visualiser'),
	

]