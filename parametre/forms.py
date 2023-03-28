# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import widgets, Textarea
from django.contrib.auth.forms import AuthenticationForm 
from django.conf import settings

from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from bootstrap_datepicker_plus import DatePickerInput
from django.utils import timezone

from parametre.models import *

from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper


class LoginForm(AuthenticationForm):
  username = forms.CharField(label="Utilisateur", max_length=40, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
  password = forms.CharField(label="Mot de passe", max_length=40, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class DateInput(forms.DateInput):
    input_type = 'date'


class OuvrageForm(ModelForm): 
    class Meta:
      model = Ouvrage
      exclude = ('valide_saisie', 'type_publication')
      widgets = {
              'titre': Textarea(attrs={'cols': 80, 'rows': 3}),

              'resume': Textarea(attrs={'cols': 80, 'rows': 5}),
              'mots_cles': Textarea(attrs={'cols': 80, 'rows': 5}),
         }

class SoutenanceForm(ModelForm):
    class Meta:
        model = Soutenance
        exclude = ('valide_saisie', 'membres', 'type_publication')
        widgets = {
          'titre': Textarea(attrs={'cols': 80, 'rows': 3}),
          'resume': Textarea(attrs={'cols': 80, 'rows': 5}),

          'date_soutenance' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),

          'ufr': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('administration:ufr_create'),
                #reverse_lazy('administration:ufr_update', args=['__fk__']),
          ),
          
          'specialite': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('administration:specialite_create'),
          ),    
          
           'laboratoire': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('administration:laboratoire_create'),
          ),    
                 
          'etablissement': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('administration:etablissement_create'),
          ),    
         
          'motcles': AddAnotherWidgetWrapper(
                forms.SelectMultiple,
                reverse_lazy('administration:motcles_create'),
        )
      }        
# COMMENT APPELER UNE FONCTION admin
#admin:{{ app_label }}_{{ model_name }}_changelist


class AuteurForm(ModelForm):

  class Meta:
      model = Auteur
      exclude = ('photo',)

class EditeurForm(ModelForm):
  class Meta:
      model = Editeur
      exclude = ('telephone', 'photo')

class ArticleForm(ModelForm):
  class Meta:
      model = Article
      exclude = ()

class MotcleForm(ModelForm):
  class Meta:
      model = Motcle
      exclude = ()


class JuryForm(ModelForm):
  #membre = forms.ModelChoiceField(required=False, queryset=Membre.objects.all())

  def __init__(self, *args, **kwargs ):
    super(JuryForm, self).__init__( *args, **kwargs )
    for field in self.fields:self.fields[field].label=''
    
  class Meta:
    model = Jury
    exclude = ('soutenance',)
    widgets = {
          'membre': AddAnotherWidgetWrapper(
                forms.Select,
                #reverse_lazy('admin:parametre_membre_add'),
                reverse_lazy('administration:membre_create'), 
          ),  

          'statut': AddAnotherWidgetWrapper(
                forms.Select,
                #reverse_lazy('admin:parametre_membre_add'),
                reverse_lazy('administration:statut_create'), 
          ),  

      }  

JuryFormSet = modelformset_factory(Jury, extra=7, form=JuryForm, can_delete=True)

class UfrForm(ModelForm):
  class Meta:
      model = Ufr
      exclude = ()


class SpecialiteForm(ModelForm):
  class Meta:
      model = Specialite
      exclude = ()


class LaboratoireForm(ModelForm):
  class Meta:
      model = Laboratoire
      exclude = ()


class DisciplineForm(ModelForm):
  class Meta:
      model = Discipline
      exclude = ()


class SocieteForm(ModelForm):
  
	class Meta:
		model=Societe
		fields= '__all__'

class MembreForm(ModelForm):
  def __init__(self, *args, **kwargs ):
    super(MembreForm, self).__init__( *args, **kwargs )
    for field in self.fields:self.fields[field].label=''
  
  class Meta:
      model = Membre
      exclude = ()
      widgets = {
              'qualification': AddAnotherWidgetWrapper(
                    forms.Select,
                    reverse_lazy('administration:qualification_create'),
              ),          
          }  



class PartenaireForm(ModelForm):
  
  class Meta:
    model=Partenaire
    fields= '__all__'


class ContactForm(ModelForm):
  
  class Meta:
    model=Contact
    exclude = ('date_contact', 'lu')

