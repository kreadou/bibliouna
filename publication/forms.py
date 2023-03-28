# -*- coding:utf-8 -*-
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.utils import timezone
from parametre.models import *

TYPES_PUBLICATIONS = [
    ('ouvrage', 'ouvrage'),
    ('thèse', 'thèse'),
    ('mémoire', 'mémoire'),
    ('article', 'article'),
    #('(tous)', '(tous)'),
   ]   

CATEGORIES = [
    ('titres', 'titres'),
    ('auteurs', 'auteurs'),
    ('éditeurs', 'éditeurs'),
    ('mots-clés', 'mots-clés'),
    ('spécialités', 'spécialités'),
    ('disciplines', 'disciplines'),
    ('contenu du document', 'contenu du document'),
]   

TYPES_PUBLICATIONS.sort(reverse=True)

class RechercheTexteForm(forms.Form):
    categorie = forms.ChoiceField(label="Rechercher par", choices = CATEGORIES, required=False, )
    texte = forms.CharField(label="Options de recherche", required=False, widget=forms.TextInput(attrs={'alert(450);': 'titre, auteur, mots-clés, spécialités'}))
    type_publication = forms.ChoiceField(label='Type de publication', choices = TYPES_PUBLICATIONS)
    
    def __init__(self, *args, **kwargs ):
        super(RechercheTexteForm, self).__init__(*args, **kwargs)
        for field in self.fields:self.fields[field].label=''