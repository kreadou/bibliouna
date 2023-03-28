# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms import widgets, Textarea
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from bootstrap_datepicker_plus import DatePickerInput
from django.utils import timezone
from actualite.models import Evenement, DocumentEvenement
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper


class EvenementForm(ModelForm): 
    class Meta:
      model = Evenement
      exclude = ()
      widgets = {
      	'titre': Textarea(attrs={'cols': 80, 'rows': 3}),
      	'resume': Textarea(attrs={'cols': 80, 'rows': 5}),              
      	'date_du' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
      	'date_au' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
      }

class DocumentEvenementForm(ModelForm):
    class Meta:
        model = DocumentEvenement
        exclude = ('evenement',)        
