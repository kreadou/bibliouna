from django.contrib.auth import views as djviews
from django.conf.urls import url
from django.urls import re_path, path
from parametre.forms import LoginForm
from parametre import views

app_name="parametre"
urlpatterns = [
    url(r'bienvenue/$', views.bienvenue, name='bienvenue'),
    url(r'accueil/$', views.accueil, name='accueil'),

    path('login', djviews.LoginView.as_view(template_name= 'login.html', authentication_form= LoginForm), name='login'),
    
    url(r'logout/$', djviews.LogoutView.as_view(next_page='parametre:login')),

    path('connexion', djviews.LoginView.as_view(template_name= 'connexion.html', authentication_form= LoginForm), name='connexion'),
    #url(r'logout/$', djviews.LogoutView.as_view(next_page='parametre:login')), 
    path('register', djviews.LoginView.as_view(template_name= 'register.html', authentication_form= LoginForm), name='register'),

    url(r'partenaire_lister/$', views.partenaire_lister, name='partenaire_lister'),

    url(r'contact_creer/$', views.contact_creer, name='contact_creer'),
    url(r'contact_lister/$', views.contact_lister, name='contact_lister'),
    
    url(r'contact_visualiser/(?P<pk>[0-9]+)/$', views.contact_visualiser, name='contact_visualiser'),
]

