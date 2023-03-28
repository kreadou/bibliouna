from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, HttpResponse
from parametre.models import *
from publication.forms import RechercheTexteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
from .filters import SoutenanceFilter

def decomposition(list_chaine="", nombre=50):
    if list_chaine:
        k=-1
        ch = ""
        chaine = ""
        for i in list_chaine:
            if len(ch+'; '+i) >= nombre:
                ch+="..."
                chaine+=ch
                ch=""
                return chaine
            else:
                ch+=i+'; '
        if ch:
            chaine+=ch
        return chaine
    return ""


def traitement(request):
    type_publication = request.GET.get('type_publication')
    categorie = request.GET.get('categorie') 
    texte = request.GET.get('texte')  
    print("TYPE = ", type_publication, ' ', 'categorie = ', categorie, ' ', 'texte = ', texte)

    # PREMIERE ENTREE DANS LE FORMULAIRE
    if type_publication==None and categorie==None and texte==None:
        var_entree = False
        type_publication='thèse'
        categorie = 'titres'
        texte = 'abidjan'
        form = RechercheTexteForm()
    else:
        var_entree = True
        form = RechercheTexteForm(initial={
            'type_publication': type_publication,
            'categorie': categorie,
            'texte': texte
            }
        )

    resultat={}
    querecherchezvous = '' 
    optionpublication = ''
    ourechercher = ''
    champ =''

    querecherchezvous = texte 
    optionpublication = type_publication
    ourechercher = categorie 

    if ourechercher=='titres':champ='titre'
    elif ourechercher=='auteurs':champ='auteur'
    elif ourechercher=='éditeurs':champ='editeur'
    elif ourechercher=='mots-clés':champ='motcles'
    elif ourechercher=='spécialités':champ='spécialités'
    elif ourechercher=='disciplines':champ='disciplines'
    elif ourechercher=='contenu du document':champ='resume'

    if optionpublication =="ouvrage":
        publication_list=Ouvrage.objects.select_related('discipline').filter(type_publication='ouvrage')
        if champ=='titre':publication_list=publication_list.filter(titre__icontains=querecherchezvous)
        elif champ=='auteur':publication_list=publication_list.filter(auteurs__nom__icontains=querecherchezvous).distinct()
        elif champ=='auteur':publication_list=publication_list.filter(editeurs__nom__icontains=querecherchezvous).distinct()
        elif champ=='motcles':publication_list=publication_list.filter(motcles__libelle__icontains=querecherchezvous).distinct()
        elif champ=='disciplines':publication_list=publication_list.filter(discipline__libelle__icontains=querecherchezvous)
        elif champ=='resume':publication_list=publication_list.filter(resume__icontains=querecherchezvous)
        element_selectionne = "Ouvrages"
        pauteurs = ""
        pediteurs = ""
        pmotcles = ""
        for i in publication_list:
            i.pauteurs = '; '.join(list(i.auteurs.values_list("nom", flat=True)))
            i.pediteurs = '; '.join(list(i.editeurs.values_list("nom", flat=True)))
            i.pmotcles = '; '.join(list(i.motcles.values_list("libelle", flat=True)))
            #print("AUTEURS ============ ", i, i.auteurs.all())
            #print("EDITEURS ============ ", i, i.editeurs.all())
            #print("mots cles ============ ", i, i.motcles.all())

    elif optionpublication == 'thèse':
        publication_list = Soutenance.objects.select_related('ufr', 'specialite', 'laboratoire', 'etablissement').filter(type_publication='thèse')
            
        if champ=='titre':publication_list=publication_list.filter(titre__icontains=querecherchezvous)
        elif champ=='auteur':publication_list=publication_list.filter(auteur__icontains=querecherchezvous)            
        elif champ=='motcles':publication_list=publication_list.filter(motcles__libelle__icontains=querecherchezvous)
        elif champ=='spécialités':publication_list=publication_list.filter(specialite__libelle__icontains=querecherchezvous)
        elif champ=='resume':publication_list=publication_list.filter(resume__icontains=querecherchezvous)
        element_selectionne = "Thèses"
        pmotcles = ""
        for i in publication_list:
            i.pmembres =  decomposition(list(i.membres.values_list("nom", flat=True)), nombre=87)#'; '.join(list(i.membres.values_list("nom", flat=True)))
            i.pmotcles = '; '.join(list(i.motcles.values_list("libelle", flat=True)))
            #print("=============================")
            #print("decom ", i.pmembres)
            #print("++++++++++++++++++++++++++++++")

    elif optionpublication =="mémoire":
        publication_list=Soutenance.objects.select_related('ufr', 'specialite', 'laboratoire', 'etablissement').filter(type_publication='mémoire') 
        if champ=='titre':publication_list=publication_list.filter(titre__icontains=querecherchezvous)
        elif champ=='auteur':publication_list=publication_list.filter(auteur__icontains=querecherchezvous)            
        elif champ=='motcles':publication_list=publication_list.filter(motcles__libelle__icontains=querecherchezvous)
        elif champ=='spécialités':publication_list=publication_list.filter(specialite__libelle__icontains=querecherchezvous)
        elif champ=='resume':publication_list=publication_list.filter(resume__icontains=querecherchezvous)
        element_selectionne = "Mémoires"    

    elif optionpublication =="article":
        publication_list=Article.objects.select_related('ufr', 'specialite', 'laboratoire', 'discipline').filter(type_publication='article')
        if champ=='titre':publication_list=publication_list.filter(titre__icontains=querecherchezvous)
        elif champ=='auteur':publication_list=publication_list.filter(auteur__icontains=querecherchezvous)            
        elif champ=='motcles':publication_list=publication_list.filter(motcles__libelle__icontains=querecherchezvous)
        elif champ=='spécialités':publication_list=publication_list.filter(specialite__libelle__icontains=querecherchezvous)
        elif champ=='resume':publication_list=publication_list.filter(resume__icontains=querecherchezvous)
        element_selectionne = "Articles"

    elif optionpublication =="(Tous)":
        element_selectionne = "(Tous)"

    ########### PAGINATION ####################
    page = request.GET.get('page', 1)
    paginator = Paginator(publication_list, per_page=10)
    page_range = paginator.page_range # this page range
    try:
        publications = paginator.get_page(page)
    except PageNotAnInteger:
        publications = paginator.page(1)
    except EmptyPage:
        publications = paginator.page(paginator.num_pages)


    if type_publication in ('ouvrage', ):
        return render(request, 'publication/ouvrage.html', locals())

    if type_publication in ('article', ):
        return render(request, 'publication/article.html', locals())

    if type_publication in ('thèse', 'mémoire'):
        return render(request, 'publication/traitement.html', locals())
    return render(request, 'publication/traitement.html', locals())


def publication_detail(request, pk):
    form = RechercheTexteForm()
    publication = get_object_or_404(Soutenance, pk=pk)
    return render(request, 'publication/publication_detail.html', locals())

def ouvrage_detail(request, pk):
    form = RechercheTexteForm()
    publication = get_object_or_404(Ouvrage, pk=pk)
    return render(request, 'publication/ouvrage_detail.html', locals())

def article_detail(request, pk):
    form = RechercheTexteForm()
    publication = get_object_or_404(Article, pk=pk)
    return render(request, 'publication/article_detail.html', locals())


def telechargement(request):
    if request.method == "GET" and request.is_ajax():
        type_publication = request.GET.get("type_publication")
        print("telechargement", type_publication)
        if type_publication in ('thèse', 'mémoire'):
            publication = get_object_or_404(Soutenance, pk=int(request.GET.get("code_publication")))          
        elif type_publication in ('ouvrage',):
            publication = get_object_or_404(Ouvrage, pk=int(request.GET.get("code_publication")))  
        elif type_publication in ('article',):
            publication = get_object_or_404(Article, pk=int(request.GET.get("code_publication"))) 
        format = request.GET.get("format")
        if publication and format:
            print("les infos = ", publication, format)
            if format=='texte':
                try:
                    print("fichier = ", publication.ftexte)
                    os.startfile(publication.ftexte.path)
                except:pass
            elif format == "pdf":
                """
                try:
                    #print("fichier = {}".format(publication.fpdf.url))
                    print("fichier path = ", publication.fpdf.path)
                    fichier = publication.fpdf.path
                    
                    #fichier = open(settings.MEDIA_ROOT + '\\fpdfs\\' + '{0}'.format(publication.fpdf, 'rb'))
                    print(fichier)
                    return FileResponse(fichier)
                except:print("Erreur 1")
                try:
                    pass#return FileResponse(publication.fpdf.path)
                except:print("Erreur 2")
                """
                #os.startfile(publication.fpdf.path)
                fichier = r'{}'.format(publication.fpdf.path)
                #fichier = "C:\\developpement\\bibliouna\\media\\fpdfs\\THESE_SOUTENUE_CORRIGEE_FINALE_SYLLA_combinée.pdf"
                print(fichier)
                os.startfile(fichier)

                with open(fichier, 'r', encoding="utf8", errors='ignore') as pdf:
                        response = HttpResponse(pdf.read(), content_type='application/pdf')
                        response['Content-Disposition'] = 'inline;filename='+fichier
                        return response
                pdf.closed
                

            elif format == "audio":
                try:
                    os.startfile(publication.faudio.path)
                except:pass
            elif format == "video":
                try:
                    print("fichier = ", publication.fvideo)
                    os.startfile(publication.fvideo.path)
                except:pass
    return JsonResponse(data={'OK':True})

"""
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from publication.serializers import SoutenanceSerializers
from parametre.models import Soutenance
from publication.pagination import StandardResultsSetPagination


def WineList(request):
	return render(request, "wine.html", {})


class SoutenanceListing(ListAPIView):
    # set the pagination and serializer class
	pagination_class = StandardResultsSetPagination
	serializer_class = SoutenanceSerializers

	def get_queryset(self):
        # filter the queryset based on the filters applied

		queryList = Soutenance.objects.all()
		titre = self.request.query_params.get('titre', None)
		#variety = self.request.query_params.get('variety', None)
		#province = self.request.query_params.get('province', None)
		#region = self.request.query_params.get('region', None)
		#sort_by = self.request.query_params.get('sort_by', None)

		if titre:
		    queryList = queryList.filter(titre = titre)
		
		if variety:
		    queryList = queryList.filter(variety = variety)
		if province:
		    queryList = queryList.filter(province = province)
		if region:
		    queryList = queryList.filter(region = region)    

        # sort it if applied on based on price/points

		if sort_by == "price":
		    queryList = queryList.order_by("price")
		elif sort_by == "points":
		    queryList = queryList.order_by("points")
	
		return queryList


def getCountries(request):
    # get all the countreis from the database excluding 
    # null and blank values

    if request.method == "GET" and request.is_ajax():
        countries = Wine.objects.exclude(country__isnull=True).\
            exclude(country__exact='').order_by('country').values_list('country').distinct()
        countries = [i[0] for i in list(countries)]
        data = {
            "countries": countries, 
        }
        return JsonResponse(data, status = 200)


def getvariety(request):
    if request.method == "GET" and request.is_ajax():
        # get all the varities from the database excluding 
        # null and blank values

        variety = Wine.objects.exclude(variety__isnull=True).\
        	exclude(variety__exact='').order_by('variety').values_list('variety').distinct()
        variety = [i[0] for i in list(variety)]
        data = {
            "variety": variety, 
        }
        return JsonResponse(data, status = 200)


def getProvince(request):
    # get the provinces for given country from the 
    # database excluding null and blank values

    if request.method == "GET" and request.is_ajax():
        country = request.GET.get('country')
        province = Wine.objects.filter(country = country).\
            	exclude(province__isnull=True).exclude(province__exact='').\
            	order_by('province').values_list('province').distinct()
        province = [i[0] for i in list(province)]
        data = {
            "province": province, 
        }
        return JsonResponse(data, status = 200)


def getRegion(request):
    # get the regions for given province from the 
    # database excluding null and blank values
    
    if request.method == "GET" and request.is_ajax():
        province = request.GET.get('province')
        region = Wine.objects.filter(province = province).\
                exclude(region__isnull=True).exclude(region__exact='').values_list('region').distinct()
        region = [i[0] for i in list(region)]
        data = {
            "region": region, 
        }
        return JsonResponse(data, status = 200)


def index(request):
	categorie = forms.ChoiceField(label="Rechercher par", choices = CATEGORIES, required=False, )
    texte = forms.CharField(label="Options de recherche", required=False, widget=forms.TextInput(attrs={'alert(450);': 'titre, auteur, mots-clés, spécialités'}))
    type_publication = forms.ChoiceField(label='Type de publication', choices = TYPES_PUBLICATIONS)
    return render(request, "base.html")
"""
