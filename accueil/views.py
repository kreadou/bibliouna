from django.shortcuts import render
from parametre.models import Partenaire


def index(request):
	partenaire_list = Partenaire.objects.all() 
	return render(request, 'accueil/base.html', locals())

def contact(request):
	return render(request, 'accueil/contact.html', locals())

def presentation(request):
	return render(request, 'accueil/presentation.html', locals())

def charte_bon_usage(request):
	return render(request, 'accueil/charte_bon_usage.html', locals())

def reglement_interieur(request):
	return render(request, 'accueil/reglement_interieur.html', locals())
