# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from . models import *
from . forms import *


def evenement_lister(request):
    evenement_list = Evenement.objects.order_by('-date_publication')
    return render(request, 'actualite/evenement_lister.html', locals())


def evenement_creer(request):
    form = EvenementForm()
    if request.method == "POST":
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evenement_lister')
        return render(request, 'actualite/evenement_creer.html', locals())
    return render(request, 'actualite/evenement_creer.html', locals())


def evenement_modifier(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    form = EvenementForm(instance=evenement)
    if request.method == "POST":
        form = EvenementForm(request.POST, request.FILES, instance=evenement)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evenement_lister')
        return render(request, 'actualite/evenement_creer.html', locals())
    return render(request, 'actualite/evenement_creer.html', locals())


def evenement_visualiser(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    document_list = DocumentEvenement.objects.filter(evenement=evenement)
    return render(request, 'actualite/evenement_visualiser.html', locals())

