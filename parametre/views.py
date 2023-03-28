# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm, modelformset_factory, formset_factory
from parametre.models import * 
from .forms import *#OuvrageForm, SoutenanceForm, AuteurForm, EditeurForm, ArticleForm, MotcleForm, JuryForm, UfrForm, \
#SpecialiteForm, LaboratoireForm, DisciplineForm 

from datetime import *
import time
from django.views import generic
import django


def index(request):
	return render(request, "base.html")

def bienvenue(request):
    return render(request, 'parametre/bienvenue.html', locals())


@login_required(login_url="parametre:login")
def accueil(request):
    return render(request, 'administration/accueil.html', locals())


def partenaire_lister(request):
    partenaire_list = Partenaire.objects.all()
    return render(request, 'parametre/partenaire.html', locals())


def contact_creer(request):
    form = ContactForm() 
    if request.method == 'POST':
        form = ContactForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('parametre/bienvenue')
    return render(request, 'parametre/contact.html', locals())


def contact_visualiser(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(instance=contact)
    return render(request, 'parametre/contact_visualiser.html', locals())


def contact_lister(request):
    contact_list = Contact.objects.order_by('lu', '-date_contact')
    return render(request, 'parametre/contact_lister.html', locals())
