from django.conf.urls import url
from django.urls import re_path, path
from django.conf import settings
from abonne import views
from django.contrib.auth.views import LogoutView


app_name="abonne"
urlpatterns = [
	path('abonne_creer/', views.abonne_creer, name='abonne_creer'),
	path('abonne_lister/', views.abonne_lister, name='abonne_lister'),

	path('abonnement', views.abonnement, name='abonnement'),
	path('abonnement_lister/', views.abonnement_lister, name='abonnement_lister'),

	path("register/", views.register, name="register"),

	path("login/", views.login_request, name="login"),
	path("logout/", views.logout_request, name="logout"),

	#path('<int:pk>/abonne_modifier/', views.AbonneProfilView.as_view(), name='abonne_modifier'),
	#path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout_request'),
]
