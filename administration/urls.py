from django.contrib.auth import views as djviews
from django.conf.urls import url
from django.urls import re_path, path
from administration import views
from parametre.forms import LoginForm

app_name="administration"
urlpatterns = [
	url(r'accueil/$', views.accueil, name='accueil'), 
	
	url(r'ouvrage_lister/$', views.ouvrage_lister, name='ouvrage_lister'),
	url(r'ouvrage_creer/$', views.ouvrage_creer, name='ouvrage_creer'),
	url(r'ouvrage_modifier/(?P<pk>[0-9]+)/$', views.ouvrage_modifier, name='ouvrage_modifier'),

	url(r'these_lister/$', views.these_lister, name='these_lister'),
	url(r'these_creer/$', views.these_creer, name='these_creer'),
	url(r'these_modifier/(?P<pk>[0-9]+)/$', views.these_modifier, name='these_modifier'),

	url(r'memoire_lister/$', views.memoire_lister, name='memoire_lister'),
	url(r'memoire_creer/$', views.memoire_creer, name='memoire_creer'),
	url(r'memoire_modifier/(?P<pk>[0-9]+)/$', views.memoire_modifier, name='memoire_modifier'),

	url(r'article_lister/$', views.article_lister, name='article_lister'),
	url(r'article_creer/$', views.article_creer, name='article_creer'),
	url(r'article_modifier/(?P<pk>[0-9]+)/$', views.article_modifier, name='article_modifier'),

	url(r'auteur_lister/$', views.auteur_lister, name='auteur_lister'),
	url(r'auteur_creer/$', views.auteur_creer, name='auteur_creer'),
	url(r'auteur_modifier/(?P<pk>[0-9]+)/$', views.auteur_modifier, name='auteur_modifier'),
	url(r'auteur_creer_popup/$', views.auteur_creer_popup, name="auteur_creer_popup"),

	url(r'editeur_lister/$', views.editeur_lister, name='editeur_lister'),
	url(r'editeur_creer/$', views.editeur_creer, name='editeur_creer'),  	
	url(r'editeur_modifier/(?P<pk>[0-9]+)/$', views.editeur_modifier, name='editeur_modifier'),
	url(r'editeur_creer_popup/$', views.editeur_creer_popup, name="editeur_creer_popup"),

	url(r'motcle/$', views.motcle, name="motcle"),
	url(r'motcle_creer_popup/$', views.motcle_creer_popup, name="motcle_creer_popup"),
	url(r'motcles_create/$', views.motcles_create.as_view(), name="motcles_create"),

	url(r'jury_lister/$', views.jury_lister, name='jury_lister'),
	url(r'jury_creer/$', views.jury_creer, name='jury_creer'),   
	url(r'jury_modifier/(?P<pk>[0-9]+)/$', views.jury_modifier, name='jury_modifier'),
	url(r'jury_creer_popup/$', views.jury_creer_popup, name="jury_creer_popup"),

	url(r'ufr_lister/$', views.ufr_lister, name='ufr_lister'),
	url(r'ufr_creer/$', views.ufr_creer, name='ufr_creer'),   
	url(r'ufr_modifier/(?P<pk>[0-9]+)/$', views.ufr_modifier, name='ufr_modifier'),
	url(r'ufr_creer_popup/$', views.ufr_creer_popup, name="ufr_creer_popup"),
	url(r'ufr/$', views.ufr, name="ufr"),
	url(r'ufr_create/$', views.ufr_create.as_view(), name="ufr_create"),
	url(r'ufr_update/(?P<pk>[0-9]+)/$', views.ufr_update.as_view(), name='ufr_update'),

	url(r'specialite_lister/$', views.specialite_lister, name='specialite_lister'),
	url(r'specialite_creer/$', views.specialite_creer, name='specialite_creer'),   
	url(r'specialite_modifier/(?P<pk>[0-9]+)/$', views.specialite_modifier, name='specialite_modifier'),
	url(r'specialite_creer_popup/$', views.specialite_creer_popup, name="specialite_creer_popup"),
	url(r'specialite/$', views.specialite, name="specialite"),
	url(r'specialite/$', views.specialite, name="specialite_edit"),
	url(r'specialite_create/$', views.specialite_create.as_view(), name="specialite_create"),

	url(r'laboratoire_lister/$', views.laboratoire_lister, name='laboratoire_lister'),
	url(r'laboratoire_creer/$', views.laboratoire_creer, name='laboratoire_creer'),   
	url(r'laboratoire_modifier/(?P<pk>[0-9]+)/$', views.laboratoire_modifier, name='laboratoire_modifier'),
	url(r'laboratoire_creer_popup/$', views.laboratoire_creer_popup, name="laboratoire_creer_popup"),
	url(r'laboratoire/$', views.laboratoire, name="laboratoire"),
	url(r'laboratoire_create/$', views.laboratoire_create.as_view(), name="laboratoire_create"),

	url(r'discipline_lister/$', views.discipline_lister, name='discipline_lister'),
	url(r'discipline_creer/$', views.discipline_creer, name='discipline_creer'),   
	url(r'discipline_modifier/(?P<pk>[0-9]+)/$', views.discipline_modifier, name='discipline_modifier'),
	url(r'discipline_creer_popup/$', views.discipline_creer_popup, name="discipline_creer_popup"),
	url(r'discipline/$', views.discipline, name="discipline"),

	url(r'membre_lister/$', views.membre_lister, name='membre_lister'),
	url(r'membre_creer/$', views.membre_creer, name='membre_creer'),   
	url(r'membre_modifier/(?P<pk>[0-9]+)/$', views.membre_modifier, name='membre_modifier'),
	url(r'membre_creer_popup/$', views.membre_creer_popup, name="membre_creer_popup"),
	url(r'membre/$', views.membre, name="membre"),
	url(r'membre_create/$', views.membre_create.as_view(), name="membre_create"),

	url(r'sauvegarde_membre/$', views.sauvegarde_membre, name="sauvegarde_membre"),

	
	url(r'delete_jury/(?P<pk>[0-9]+)/$', views.delete_jury, name="delete_jury"),

	url(r'create_jury_form/$', views.create_jury_form, name="create_jury_form"),
	
	
	url(r'etablissement_create/$', views.etablissement_create.as_view(), name="etablissement_create"),
	
	
	url(r'qualification_create/$', views.qualification_create.as_view(), name="qualification_create"),

	url(r'statut_lister/$', views.statut_lister, name="statut_lister"),

	url(r'statut_create/$', views.statut_create.as_view(), name="statut_create"),
]


