from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Abonne, Abonnement

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AbonneForm(forms.ModelForm):
    class Meta:
        model = Abonne
        exclude = ('user', 'matricule')


class AbonnementForm(forms.ModelForm):
    class Meta:
        model = Abonnement
        exclude = ()
        widgets = {
           'date_debut' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_fin' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
          } 


class AbonneProfilForm(UserChangeForm):
    password = None
    class Meta:
        model = Abonne
        fields = '__all__'


