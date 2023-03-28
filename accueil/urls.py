from django.conf.urls import url 
from django.urls import re_path, path
from accueil import views

app_name="accueil"
urlpatterns = [
	path('', views.index, name='index'),
	path('contact/', views.contact, name='contact'),
	path('presentation/', views.presentation, name='presentation'),
	path('charte_bon_usage/', views.charte_bon_usage, name='charte_bon_usage'),
	path('reglement_interieur/', views.reglement_interieur, name='reglement_interieur'),

]