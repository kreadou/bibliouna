from django.urls import re_path, path
from django.conf import settings
from django.conf.urls.static import static

from galerie import views

app_name="galerie"
urlpatterns = [
	path('index/', views.index, name='index'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
]


