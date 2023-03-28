# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm, inlineformset_factory, modelformset_factory, formset_factory
from django.views import generic
from parametre.models import * 
from parametre.forms import * #OuvrageForm, SoutenanceForm, AuteurForm, EditeurForm, ArticleForm, MotcleForm, JuryForm, UfrForm, \
#SpecialiteForm, LaboratoireForm, DisciplineForm 
from django.conf import settings
from datetime import *
import time
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods

from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from pdf2image import convert_from_path

import fitz

from django.db import transaction, IntegrityError
motclesFormSet = modelformset_factory(Motcle, extra=7, exclude=())

#mot_cles = tuple(Motcle.objects.values_list('libelle').all())
#print(mot_cles)

STATUTS = (
    ('Président', 'Président'),
    ('Directeur', 'Directeur'),
    ('Co-Directeur', 'Co-Directeur'),
    ("Rapporteur", "Rapporteur"),
    ("Examinateur", "Examinateur"),
    ("Coordinateur", "Coordinateur"),
    ("Evaluateur", "Evaluateur"),
  )  

#print("statuts ok", Statut.objects.all())#.delete())
#for i in STATUTS: Statut.objects.create(libelle=i[1])
"""
for i in Jury.objects.all():
    #print(i.statut)
    print(Statut.objects.get(libelle=i.statut)) 
    i.statute=Statut.objects.get(libelle=i.statut)
    i.save()
"""

from Utilitaire import dicovar

try:
   fichierPara = dicovar("pygesys.dll")
   #print("lecture du dictionnaire des parametres réussi...")
except:pass

k=0
"""
#print('ooooooooooooooooooooooooo', Soutenance.objects.exclude(fpdf='').count())
#print('ooooooooooooooooooooooooo', Soutenance.objects.filter(fpdf='').count())
for these in Soutenance.objects.exclude(fpdf=''):
    if these.fpdf and not these.photo:
        k+=1
        #print(k, "ceux dui nont pas de photo", these.titre)
        try:
            print("entree")    
            pdffile = these.fpdf.path
            doc = fitz.open(pdffile)
            page = doc.loadPage(0)  # number of page
            pix = page.get_pixmap()
            #pix.save('/home1/bibliowad/public_html/media/theses/'+these.fpdf.name[6:-4]+'.jpg')
            try:
                these.photo = 'theses/'+these.fpdf.name[6:-4]+'.jpg'
                these.save()
            except:t("erreur 1 = ", k)
        except:print("erreur 2 = ", k)
#'/home1/bibliowad/public_html/static'
#####################################
"""

class membre_create(CreatePopupMixin, CreateView):
    model = Membre
    template_name = "administration/membre_creer_popup.html"
    fields = ('nom', 'qualification')


class specialite_create(CreatePopupMixin, CreateView):
    model = Specialite
    template_name = "administration/specialite_creer_popup.html"
    fields = ('libelle',)


class EditSpecialite(UpdatePopupMixin, generic.UpdateView):
    model = Specialite
    fields = ['libelle']


class ufr_create(CreatePopupMixin, CreateView):
    model = Ufr
    template_name = "administration/ufr_creer_popup.html"
    fields = ('libelle', 'abrege')

class ufr_update(UpdatePopupMixin, generic.UpdateView):
    model = Ufr
    template_name = "administration/ufr_update_popup.html"
    fields = ('libelle', 'abrege')
    #success_url = "/ufr/{ufr_id}"

class laboratoire_create(CreatePopupMixin, CreateView):
    model = Laboratoire
    template_name = "administration/laboratoire_creer_popup.html"
    fields = ('libelle', 'abrege')


class etablissement_create(CreatePopupMixin, CreateView):
    model = Etablissement
    template_name = "administration/etablissement_creer_popup.html"
    fields = ('libelle', 'abrege')

class motcles_create(CreatePopupMixin, CreateView):
    model = Motcle
    template_name = "administration/motcle_creer_popup.html"
    form = motclesFormSet()
    fields = ('libelle',)
    
    """
    def get_context_data(self, **kwargs):
        context = super(motcles_create, self).get_context_data(**kwargs)
        context['formset'] = motclesFormSet(queryset=Motcle.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = motclesFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        return HttpResponseRedirect('/')
    """


class qualification_create(CreatePopupMixin, CreateView):
    model = Qualification
    template_name = "administration/qualification_creer_popup.html"
    fields = ('libelle',)


class statut_create(CreatePopupMixin, CreateView):
    model = Statut
    template_name = "administration/statut_creer_popup.html"
    fields = ('libelle',)


def convert_pdf_image(fichier):
    print('nom du fichier = ', fichier)
    img = None
    if fichier:
        #pages = convert_from_path(settings.MEDIA_ROOT+'\\fpdfs\\'+fichier, dpi=500, poppler_path=r"C:\\developpement\\bibliowad\\poppler-0.68.0\\bin")
        pages = convert_from_path(fichier, dpi=500, poppler_path=r"C:\\developpement\\bibliowad\\poppler-0.68.0\\bin")
        
        page = pages[0]
        page.save('page_garde.jpg', 'JPEG')
    return page  
    #from pdf2image import convert_from_path
    #images = convert_from_path('WEB SERVER SIGMA LITE SERIES.pdf', 500, poppler_path=r'C:\developpement\bibliowad\poppler-0.68.0\bin')
    #images[0].save('page.jpg', 'JPEG')


@login_required(login_url="parametre:login")
def accueil(request):
    utilisateur_group = request.user.groups.values_list('name', flat=True)
    print("users group = ", utilisateur_group) 
    return render(request, 'administration/accueil.html', locals())


def ouvrage_lister(request):
    ouvrage_list = Ouvrage.objects.order_by('titre')
    return render(request, 'administration/ouvrage_lister.html', locals())

def ouvrage_creer(request):
    if request.method =='POST':
        form = OuvrageForm(request.POST, request.FILES)
        if form.is_valid():
            ouvrage = form.save(commit=False)
            ouvrage.type_publication = 'ouvrage'
            ouvrage.save()
            return HttpResponseRedirect('ouvrage_lister')
        return render(request, 'administration/ouvrage_creer.html', locals())
    form = OuvrageForm()
    return render(request, 'administration/ouvrage_creer.html', locals())


def ouvrage_modifier(request, pk):
    ouvrage = get_object_or_404(Ouvrage, pk=pk)
    if request.method =='POST':
        form = OuvrageForm(request.POST, request.FILES, instance=ouvrage)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('ouvrage_lister')
        else:
            return render(request, 'administration/ouvrage_modifier.html', locals())
    else:
        form = OuvrageForm(instance=ouvrage)
    return render(request, 'administration/ouvrage_modifier.html', locals())


def these_lister(request):
    these_list = Soutenance.objects.filter(type_publication='thèse').select_related(
        'ufr', 'specialite', 'laboratoire', 'etablissement', #'motcles', 'membres'
        ).order_by('-id')[:]
    return render(request, 'administration/these_lister.html', locals())


def add_more_membre(request):
    extra = int(float(request.GET['extra'])) + 1
    form = SoutenanceForm(initial=request.POST)
    JuryFormSet = modelformset_factory(Jury, extra=extra, form=JuryForm, can_delete=True)
    juryformset = JuryFormSet(queryset=Jury.objects.filter(soutenance__id=0))
    return render(request, 'administration/these_creer.html', locals())

def create_jury_form(request):
    form = JuryForm()
    context = {"form": form}
    return render(request, "administration/partial/jury_form.html", context)

"""
if 'add_jury' in request.POST:
cp = request.POST.copy()
cp['jury-TOTAL_FORMS'] = int(cp['jury-TOTAL_FORMS'])+ 1
new_jury = AddCarFormset(cp, prefix='jury')

    trajetFormSet = modelformset_factory(Trajet, extra=3, exclude=())
    if request.method=="POST" and request.POST.get("submit")=="ligne":
        if request.POST.get("ligne"):
            nombre_ligne = request.POST.get("ligne")
            #print("nombre de ligne = ", request.POST.get("ligne"))
            trajetFormSet = modelformset_factory(Trajet, extra=int(nombre_ligne), exclude=())

"""
def these_creer(request):
    if request.method =='POST':
        form = SoutenanceForm(request.POST, request.FILES)
        formset = JuryFormSet(request.POST, queryset=Jury.objects.none())
        #print("errors", formset)
        #print("VALIDE ", len(list(filter(lambda x : x.cleaned_data, formset))))
        #print("ok ", list(filter(lambda x : x.is_valid(), formset)))
        if form.is_valid() and all(list(filter(lambda x : x.is_valid(), formset))):
            these = form.save(commit=False)
            these.type_publication = 'thèse'
            these.save()
            if these.fpdf:
                print('222', these.fpdf)
                print('222', these.photo)
                
                pages = convert_from_path(these.fpdf.path, dpi=500, poppler_path=r"C:\developpement\bibliowad\poppler-0.68.0\bin")
            
                page = pages[0]
                foto = page.save(settings.MEDIA_ROOT + '\\theses\\'+these.fpdf.name[6:-4]+'.jpg')
    
                """
                blob = BytesIO()
                rendered_image.save(blob, 'PNG')
                image_field.delete(save=False)
                image_field.save('Image.png', File(blob))
                """
                #photo.image.save(name, content, save=True)
                try:
                    these.photo = settings.MEDIA_ROOT + '\\theses\\'+these.fpdf.name[6:-4]+'.jpg'
                    these.save()
                except:pass 
                #these.photo = page
                #print('555', page)
                #these.save()
            for instance in list(filter(lambda x : x.is_valid(), formset)):
                try:
                    print('02222')
                    jury = instance.save(commit=False)
                    jury.soutenance = these
                    print('444444')
                    jury.save()
                    print('00000001', jury.statut)
                except:pass    
                
            if 'enregistrer_saisie' in request.POST:
                form = SoutenanceForm()
                #form.fields['type_publication'].choices=[('thèse', 'thèse')]
                formset = JuryFormSet(queryset=Jury.objects.none())
                formset[0].fields['statut'].choices=[('Président', 'Président')]
                for j in range(1, len(formset)):
                    formset[j].fields['statut'].choices=STATUTS[1:]#[('Directeur', 'Directeur'), ('Rapporteur', 'Rapporteur'),]
                return render(request, 'administration/these_creer.html', locals())
            else:
                return HttpResponseRedirect('these_lister')
        else:
            return render(request, 'administration/these_creer.html',  locals())
    else:
        form = SoutenanceForm()
        #form.fields['type_publication'].choices=[('thèse', 'thèse')]
        formset = JuryFormSet(queryset=Jury.objects.none())
        formset[0].fields['statut'].choices=[(i.id, i.libelle) for i in Statut.objects.filter(libelle='Président')]#(Statut.objects.filter(libelle='Président')[0].id, Statut.objects.filter(libelle='Président')[0].libelle)]
        for j in range(1, len(formset)):
            formset[j].fields['statut'].choices=[(i.id, i.libelle) for i in Statut.objects.exclude(libelle='Président')]#,STATUTS[1:]#[('Directeur', 'Directeur'), ('Rapporteur', 'Rapporteur'),]
        return render(request, 'administration/these_creer.html', locals())


def these_modifier(request, pk):
    soutenance = get_object_or_404(Soutenance, pk=pk)
    if request.method =='POST':
        form = SoutenanceForm(request.POST, request.FILES, instance=soutenance)
        formset = JuryFormSet(request.POST, queryset=Jury.objects.filter(soutenance=soutenance))
        #print("errors", formset)
        #print("VALIDE ", len(list(filter(lambda x : x.cleaned_data, formset))))
        #print("ok ", list(filter(lambda x : x.is_valid(), formset)))
        if form.is_valid() and all(list(filter(lambda x : x.is_valid(), formset))):
            #these = form.save(commit=False)
            #these.type_publication = 'thèse'
            form.save()
            for instance in list(filter(lambda x : x.is_valid(), formset)):
                try:
                    jury = instance.save(commit=False)
                    jury.soutenance = soutenance
                    jury.save()
                except:pass    
            return HttpResponseRedirect('these_lister')
        else:
            return render(request, 'administration/these_modifier.html',  locals())
    else:
        form = SoutenanceForm(instance=soutenance) #initial={'date_soutenance':soutenance.date_soutenance})
        formset = JuryFormSet(queryset=Jury.objects.filter(soutenance=soutenance))
        #formset[0].fields['statut'].choices=[('Président', 'Président')]
        #for j in range(1, len(formset)):
        #    formset[j].fields['statut'].choices=STATUTS[1:]#[('Directeur', 'Directeur'), ('Rapporteur', 'Rapporteur'),]
        return render(request, 'administration/these_modifier.html', locals())


def memoire_lister(request):
    memoire_list = Soutenance.objects.filter(type_publication='mémoire').select_related(
        'ufr', 'specialite', 'laboratoire', 'etablissement',
        ).order_by('-id')
    return render(request, 'administration/memoire_lister.html', locals())


def memoire_creer(request):
    if request.method =='POST':
        form = SoutenanceForm(request.POST, request.FILES)
        formset = JuryFormSet(request.POST, queryset=Jury.objects.none())
        if form.is_valid() and all(list(filter(lambda x : x.is_valid(), formset))):
            memoire = form.save(commit=False)
            memoire.type_publication = 'mémoire'
            memoire.save()
            if memoire.fpdf:
                pages = convert_from_path(memoire.fpdf.path, dpi=500, poppler_path=r"C:\developpement\bibliowad\poppler-0.68.0\bin")
                page = pages[0]
                foto = page.save(settings.MEDIA_ROOT + '\\memoires\\'+memoire.fpdf.name[6:-4]+'.jpg')
                try:
                    memoire.photo = settings.MEDIA_ROOT + '\\memoires\\'+memoire.fpdf.name[6:-4]+'.jpg'
                    memoire.save()
                except:pass 
            for instance in list(filter(lambda x : x.is_valid(), formset)):
                try:
                    jury = instance.save(commit=False)
                    jury.soutenance = memoire
                    jury.save()
                except:pass    
                
            if 'enregistrer_saisie' in request.POST:
                form = SoutenanceForm()
                formset = JuryFormSet(queryset=Jury.objects.none())
                formset[0].fields['statut'].choices=[('Président', 'Président')]
                for j in range(1, len(formset)):
                    formset[j].fields['statut'].choices=STATUTS[1:]#[('Directeur', 'Directeur'), ('Rapporteur', 'Rapporteur'),]
                return render(request, 'administration/these_creer.html', locals())
            else:
                return HttpResponseRedirect('memoire_lister')
        else:
            return render(request, 'administration/memoire_creer.html',  locals())
    else:
        form = SoutenanceForm()
        formset = JuryFormSet(queryset=Jury.objects.none())
        formset[0].fields['statut'].choices=[(i.id, i.libelle) for i in Statut.objects.filter(libelle='Président')]#(Statut.objects.filter(libelle='Président')[0].id, Statut.objects.filter(libelle='Président')[0].libelle)]
        for j in range(1, len(formset)):
            formset[j].fields['statut'].choices=[(i.id, i.libelle) for i in Statut.objects.exclude(libelle='Président')]#,STATUTS[1:]#[('Directeur', 'Directeur'), ('Rapporteur', 'Rapporteur'),]
        return render(request, 'administration/memoire_creer.html', locals())


def memoire_modifier(request, pk):
    memoire = soutenance = get_object_or_404(Soutenance, pk=pk)
    if request.method =='POST':
        form = SoutenanceForm(request.POST, request.FILES, instance=soutenance)
        formset = JuryFormSet(request.POST, queryset=Jury.objects.filter(soutenance=soutenance))
        if form.is_valid() and all(list(filter(lambda x : x.is_valid(), formset))):
            form.save()
            for instance in list(filter(lambda x : x.is_valid(), formset)):
                try:
                    jury = instance.save(commit=False)
                    jury.soutenance = soutenance
                    jury.save()
                except:pass    
            return HttpResponseRedirect('memoire_lister')
        else:
            return render(request, 'administration/memoire_modifier.html',  locals())
    else:
        form = SoutenanceForm(instance=soutenance)
        formset = JuryFormSet(queryset=Jury.objects.filter(soutenance=soutenance))
    return render(request, 'administration/memoire_modifier.html', locals())


def article_lister(request):
    article_list = Article.objects.select_related('ufr', 'specialite', 'laboratoire', 'discipline').order_by('-id')
    return render(request, 'administration/article_lister.html', locals())


def article_creer(request):
    if request.method =='POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('article_lister')
        else:
            return render(request, 'administration/article_creer.html', {'form':form})
    else:
        form = ArticleForm()
        form.fields['type_publication'].choices=[('article', 'article')]
    return render(request, 'administration/article_creer.html', locals())

def article_modifier(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method =='POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('article_lister')
        else:
            return render(request, 'administration/article_modifier.html', locals())
    else:
        form = ArticleForm(instance=article)
    return render(request, 'administration/article_modifier.html', locals())


def auteur_lister(request):
    auteur_list = Auteur.objects.all()
    return render(request, 'administration/auteur_lister.html', locals())

def auteur_creer(request):
    if request.method =='POST':
        form = AuteurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('auteur_lister')
        else:
            return render(request, 'administration/auteur_creer.html', {'form':form})
    else:
        form = AuteurForm()
    return render(request, 'administration/auteur_creer.html', locals())

def auteur_modifier(request, pk):
    auteur = get_object_or_404(Auteur, pk=pk)
    if request.method =='POST':
        form = AuteurForm(request.POST, request.FILES, instance=auteur)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('auteur_lister')
        else:
            return render(request, 'administration/auteur_modifier.html', locals())
    else:
        form = AuteurForm(instance=auteur)
    return render(request, 'administration/auteur_modifier.html', locals())


def auteur_creer_popup(request):
    if request.method == 'POST':
        form = AuteurForm(request.POST or None)
        if form.is_valid():
            auteur = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (auteur.pk, auteur.nom+' '+auteur.prenoms, 0))
        else:
            return render(request, 'administration/auteur_creer_popup.html', locals())
    else:
        form = AuteurForm()
        return render(request, 'administration/auteur_creer_popup.html', locals())

def AuthorCreatePopup(request):
    form = AuteurForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_author". This is the element id in the form
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))
    return render(request, "author_form.html", {"form" : form})

def AuthorEditPopup(request, pk = None):
    instance = get_object_or_404(Auteur, pk = pk)
    form = AuteurForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_author". This is the element id in the form
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))
    return render(request, "author_form.html", {"form" : form})

@csrf_exempt
def get_author_id(request):
    if request.is_ajax():
        author_name = request.GET['author_name']
        author_id = Auteur.objects.get(name = author_name).id
        data = {'author_id':author_id,}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def editeur_lister(request):
    editeur_list = Editeur.objects.all()
    return render(request, 'administration/editeur_lister.html', locals())


def editeur_creer(request):
    if request.method =='POST':
        form = EditeurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('editeur_lister')
        else:
            return render(request, 'administration/editeur_creer.html', {'form':form})
    else:
        form = EditeurForm()
    return render(request, 'administration/editeur_creer.html', locals())


def editeur_modifier(request, pk):
    editeur = get_object_or_404(Editeur, pk=pk)
    if request.method =='POST':
        form = EditeurForm(request.POST, request.FILES, instance=editeur)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('editeur_lister')
        else:
            return render(request, 'administration/editeur_modifier.html', locals())
    else:
        form = EditeurForm(instance=editeur)
    return render(request, 'administration/editeur_modifier.html', locals())


def editeur_creer_popup(request):
    if request.method == 'POST':
        form = EditeurForm(request.POST or None)
        if form.is_valid():
            editeur = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (editeur.pk, editeur.nom, 1))
        else:
            return render(request, 'administration/editeur_creer_popup.html', locals())
    else:
        form = EditeurForm()
        return render(request, 'administration/editeur_creer_popup.html', locals())

def motcle_creer_popup(request):
    if request.method == 'POST':
        form = MotcleForm(request.POST or None)
        if form.is_valid():
            motcle = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (motcle.pk, motcle.libelle, 2))
        else:
            return render(request, 'administration/motcle_creer_popup.html', locals())
    else:
        form = MotcleForm()
        return render(request, 'administration/motcle_creer_popup.html', locals())


def motcle(request):
    motcleFormSet = modelformset_factory(Motcle, extra=10, exclude=())
    formset = motcleFormSet(queryset=Motcle.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = motcleFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = motcleFormSet(queryset=Motcle.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/motcle.html', locals())
    return render(request, 'administration/motcle.html', locals())


def jury_lister(request):
    jury_list = Jury.objects.all()
    return render(request, 'administration/jury_lister.html', locals())

def jury_creer(request):
    if request.method =='POST':
        form = JuryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('jury_lister')
        else:
            return render(request, 'administration/jury_creer.html', {'form':form})
    else:
        form = JuryForm()
    return render(request, 'administration/jury_creer.html', locals())

def jury_modifier(request, pk):
    jury = get_object_or_404(Jury, pk=pk)
    if request.method =='POST':
        form = JuryForm(request.POST, request.FILES, instance=jury)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('jury_lister')
        else:
            return render(request, 'administration/jury_modifier.html', locals())
    else:
        form = JuryForm(instance=jury)
    return render(request, 'administration/jury_modifier.html', locals())


def jury_creer_popup(request):
    if request.method == 'POST':
        form = JuryForm(request.POST or None)
        if form.is_valid():
            jury = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (jury.pk, jury.nom+' '+jury.prenoms, 0))
        else:
            return render(request, 'administration/jury_creer_popup.html', locals())
    else:
        form = JuryForm()
        return render(request, 'administration/jury_creer_popup.html', locals())

def ufr_lister(request):
    ufr_list = Ufr.objects.all()
    return render(request, 'administration/ufr_lister.html', locals())

def ufr_creer(request):
    if request.method =='POST':
        form = UfrForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('ufr_lister')
        else:
            return render(request, 'administration/ufr_creer.html', {'form':form})
    else:
        form = UfrForm()
    return render(request, 'administration/jury_creer.html', locals())

def ufr_modifier(request, pk):
    ufr = get_object_or_404(Ufr, pk=pk)
    if request.method =='POST':
        form = UfrForm(request.POST, request.FILES, instance=ufr)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('ufr_lister')
        else:
            return render(request, 'administration/ufr_modifier.html', locals())
    else:
        form = UfrForm(instance=ufr)
    return render(request, 'administration/ufr_modifier.html', locals())


def ufr_creer_popup(request):
    if request.method == 'POST':
        form = UfrForm(request.POST or None)
        if form.is_valid():
            ufr = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (ufr.pk, ufr.libelle, 1))
        else:
            return render(request, 'administration/ufr_creer_popup.html', locals())
    else:
        form = UfrForm()
        return render(request, 'administration/ufr_creer_popup.html', locals())

def ufr(request):
    ufrFormSet = modelformset_factory(Ufr, extra=3, exclude=())
    formset = ufrFormSet(queryset=Ufr.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = ufrFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = ufrFormSet(queryset=Ufr.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/ufr.html', locals())
    return render(request, 'administration/ufr.html', locals())


def specialite_lister(request):
    specialite_list = Specialite.objects.all()
    return render(request, 'administration/specialite_lister.html', locals())

def specialite_creer(request):
    if request.method =='POST':
        form = SpecialiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('specialite_lister')
        else:
            return render(request, 'administration/specialite_creer.html', {'form':form})
    else:
        form = SpecialiteForm()
    return render(request, 'administration/specialite_creer.html', locals())

def specialite_modifier(request, pk):
    specialite = get_object_or_404(Specialite, pk=pk)
    if request.method =='POST':
        form = SpecialiteForm(request.POST, request.FILES, instance=specialite)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('specialite_lister')
        else:
            return render(request, 'administration/specialite_modifier.html', locals())
    else:
        form = SpecialiteForm(instance=specialite)
    return render(request, 'administration/specialite_modifier.html', locals())

def specialite_creer_popup(request):
    if request.method == 'POST':
        form = SpecialiteForm(request.POST or None)
        if form.is_valid():
            specialite = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (specialite.pk, specialite.libelle, 2))
        else:
            return render(request, 'administration/specialite_creer_popup.html', locals())
    else:
        form = SpecialiteForm()
        return render(request, 'administration/specialite_creer_popup.html', locals())

def specialite(request):
    specialiteFormSet = modelformset_factory(Specialite, extra=5, exclude=())
    formset = specialiteFormSet(queryset=Specialite.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = specialiteFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = specialiteFormSet(queryset=Specialite.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/specialite.html', locals())
    return render(request, 'administration/specialite.html', locals())


def laboratoire_lister(request):
    laboratoire_list = Laboratoire.objects.all()
    return render(request, 'administration/laboratoire_lister.html', locals())

def laboratoire_creer(request):
    if request.method =='POST':
        form = LaboratoireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('laboratoire_lister')
        else:
            return render(request, 'administration/laboratoire_creer.html', {'form':form})
    else:
        form = LaboratoireForm()
    return render(request, 'administration/laboratoire_creer.html', locals())

def laboratoire_modifier(request, pk):
    laboratoire = get_object_or_404(Laboratoire, pk=pk)
    if request.method =='POST':
        form = LaboratoireForm(request.POST, request.FILES, instance=laboratoire)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('laboratoire_lister')
        else:
            return render(request, 'administration/laboratoire_modifier.html', locals())
    else:
        form = LaboratoireForm(instance=laboratoire)
    return render(request, 'administration/laboratoire_modifier.html', locals())

def laboratoire_creer_popup(request):
    if request.method == 'POST':
        form = LaboratoireForm(request.POST or None)
        if form.is_valid():
            laboratoire = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (laboratoire.pk, laboratoire.libelle+' '+laboratoire.abrege, 3))
        else:
            return render(request, 'administration/laboratoire_creer_popup.html', locals())
    else:
        form = LaboratoireForm()
        return render(request, 'administration/laboratoire_creer_popup.html', locals())


def laboratoire(request):
    laboratoireFormSet = modelformset_factory(Laboratoire, extra=3, exclude=())
    formset = laboratoireFormSet(queryset=Laboratoire.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = laboratoireFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = laboratoireFormSet(queryset=Laboratoire.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/laboratoire.html', locals())
    return render(request, 'administration/laboratoire.html', locals())


def discipline_lister(request):
    discipline_list = Discipline.objects.all()
    return render(request, 'administration/discipline_lister.html', locals())

def discipline_creer(request):
    if request.method =='POST':
        form = DisciplineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('discipline_lister')
        else:
            return render(request, 'administration/discipline_creer.html', {'form':form})
    else:
        form = DisciplineForm()
    return render(request, 'administration/discipline_creer.html', locals())

def discipline_modifier(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    if request.method =='POST':
        form = DisciplineForm(request.POST, request.FILES, instance=discipline)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('discipline_lister')
        else:
            return render(request, 'administration/discipline_modifier.html', locals())
    else:
        form = DisciplineForm(instance=jury)
    return render(request, 'administration/discipline_modifier.html', locals())


def discipline_creer_popup(request):
    if request.method == 'POST':
        form = DisciplineForm(request.POST or None)
        if form.is_valid():
            discipline = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (discipline.pk, discipline.libelle, 4))
        else:
            return render(request, 'administration/discipline_creer_popup.html', locals())
    else:
        form = DisciplineForm()
        return render(request, 'administration/discipline_creer_popup.html', locals())

def discipline(request):
    disciplineFormSet = modelformset_factory(Discipline, extra=3, exclude=())
    formset = disciplineFormSet(queryset=Discipline.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = disciplineFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = disciplineFormSet(queryset=Discipline.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/discipline.html', locals())
    return render(request, 'administration/discipline.html', locals())


def membre_lister(request):
    membre_list = Membre.objects.all()
    return render(request, 'administration/membre_lister.html', locals())


def membre_creer(request):
    if request.method =='POST':
        form = MembreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('membre_lister')
        else:
            return render(request, 'administration/membre_creer.html', {'form':form})
    else:
        form = MembreForm()
    return render(request, 'administration/membre_creer.html', locals())


def membre_modifier(request, pk):
    membre = get_object_or_404(Membre, pk=pk)
    if request.method =='POST':
        form = MembreForm(request.POST, request.FILES, instance=membre)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('membre_lister')
        else:
            return render(request, 'administration/membre_modifier.html', locals())
    else:
        form = MembreForm(instance=membre)
    return render(request, 'administration/membre_modifier.html', locals())


def membre_creer_popup(request):
    if request.method == 'POST':
        form = MembreForm(request.POST or None)
        name = fichierPara['name_membre']
        print(" form - o = ", name)
        if form.is_valid():
            membre = form.save()
            return HttpResponse('<script>opener.dismissAddAnotherPopup(window, "%s", "%s", "%i");</script>' % (membre.pk, membre.nom, 0))
        else:
            return render(request, 'administration/membre_creer_popup.html', locals())
    else:
        form = MembreForm()
        return render(request, 'administration/membre_creer_popup.html', locals())


### UNE REQUETE AJAX SIMPLE RETURNANT UN TABLEAU HTML
def sauvegarde_membre(request):
    print('valeur ok = ', request.GET.get('membre_nom'))
    membre_nom = request.GET.get('membre_nom')
    try:
        fichierPara['membre_nom'] = membre_nom
        data = {'resultat':True}
    except:data = {'resultat':False}
    return JsonResponse(data)


def AuthorCreatePopup(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_author". This is the element id in the form
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))
    
    return render(request, "author_form.html", {"form" : form})


def membre(request):
    membreFormSet = modelformset_factory(Membre, extra=5, exclude=())
    formset = membreFormSet(queryset=Membre.objects.order_by('nom'))
    for i in formset:
        i.fields['nom'].widget.attrs.update(size='100%')
        i.fields['qualification'].widget.attrs.update(size='1%')
    if request.method=='POST':
        formset = membreFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['nom']), formset):
                i.save()
            formset = membreFormSet(queryset=Membre.objects.order_by('nom'))
            for i in formset:
                i.fields['nom'].widget.attrs.update(size='100%')
                i.fields['qualification'].widget.attrs.update(size='1%')
            return render(request, 'administration/membre.html', locals())
    return render(request, 'administration/membre.html', locals())


def continent(request):
    continentFormSet = modelformset_factory(Continent, extra=3, exclude=())
    formset = continentFormSet(queryset=Continent.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='80%')
        i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = continentFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = continentFormSet(queryset=Continent.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='80%')
                i.fields['abrege'].widget.attrs.update(size='40%')
            return render(request, 'administration/continent.html', locals())
    return render(request, 'administration/continent.html', locals())


def pays(request):
    paysFormSet = modelformset_factory(Pays, extra=3, exclude=())
    formset = paysFormSet(queryset=Pays.objects.order_by('libelle'))
    for i in formset:
        #i.fields['continent'].widget.attrs.update(size='30%',)
        i.fields['libelle'].widget.attrs.update(size='70%')
        i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = paysFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = paysFormSet(queryset=Pays.objects.order_by('libelle'))
            for i in formset:
                #i.fields['continent'].widget.attrs.update(size='30%',)
                i.fields['libelle'].widget.attrs.update(size='70%')
                i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'administration/pays.html', locals())
    return render(request, 'administration/pays.html', locals())


def region(request):
    regionFormSet = modelformset_factory(Region, extra=3, exclude=())
    formset = regionFormSet(queryset=Region.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='70%')
        i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = regionFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = regionFormSet(queryset=Region.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='70%')
                i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'administration/region.html', locals())
    return render(request, 'administration/region.html', locals())


def departement(request):
    departementFormSet = modelformset_factory(Departement, extra=3, exclude=())
    formset = departementFormSet(queryset=Departement.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='70%')
        i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = departementFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = departementFormSet(queryset=Departement.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='70%')
                i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'administration/departement.html', locals())
    return render(request, 'administration/departement.html', locals())


def ville(request):
    villeFormSet = modelformset_factory(Ville, extra=3, exclude=())
    formset = villeFormSet(queryset=Ville.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='70%')
        i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = villeFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = villeFormSet(queryset=Ville.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='70%')
                i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'administration/ville.html', locals())
    return render(request, 'administration/ville.html', locals())


def commune(request):
    communeFormSet = modelformset_factory(Commune, extra=3, exclude=())
    formset = communeFormSet(queryset=Commune.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='70%')
        i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = communeFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = communeFormSet(queryset=Commune.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='70%')
                i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'administration/commune.html', locals())
    return render(request, 'administration/commune.html', locals())


def civilite(request):
    civiliteFormSet = modelformset_factory(Civilite, extra=3, exclude=())
    formset = civiliteFormSet(queryset=Civilite.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='80%')
        i.fields['abrege'].widget.attrs.update(size='40%')

    if request.method=='POST':
        formset = civiliteFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = civiliteFormSet(queryset=Civilite.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='80%')
                i.fields['abrege'].widget.attrs.update(size='40%')

            return render(request, 'administration/civilite.html', locals())
    return render(request, 'administration/civilite.html', locals())


def fonction(request):
    fonctionFormSet = modelformset_factory(Fonction, extra=3, exclude=())
    formset = fonctionFormSet(queryset=Fonction.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = fonctionFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = fonctionFormSet(queryset=Fonction.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/fonction.html', locals())
    return render(request, 'administration/fonction.html', locals())


def profession(request):
    professionFormSet = modelformset_factory(Profession, extra=3, exclude=())
    formset = professionFormSet(queryset=Profession.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = professionFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = professionFormSet(queryset=Profession.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'administration/profession.html', locals())
    return render(request, 'administration/profession.html', locals())



def statut_lister(request):
    statutFormSet = modelformset_factory(Statut, extra=3, exclude=())
    formset = statutFormSet(queryset=Statut.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = statutFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
        
            formset = statutFormSet(queryset=Statut.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
            
            return render(request, 'administration/statut.html', locals())
    return render(request, 'administration/statut.html', locals())


def societe(request):
    try:
        societe = get_object_or_404(Societe, pk=1)
    except:
        Societe.objects.create(raisonSociale='EXPERTIS CONSULTING').save()
        societe = get_object_or_404(Societe, pk=1)  
    if request.method=='POST':
        form = SocieteForm(request.POST, instance=societe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("administration/index")
        else:return render(request, 'administration/societe.html', locals())
    else:
        form = SocieteForm(instance=societe)
        return render(request, 'administration/societe.html', locals())


@require_http_methods(['DELETE'])
def delete_jury(request, pk):
    Jury.objects.filter(id=pk).delete()
    juryformset = JuryFormSet(queryset=Jury.objects.filter(soutenance__id=pk))
    return render(request, 'administration/partial/partial_jury_lister.html', {'juryformset': juryformset})

