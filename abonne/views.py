from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Abonne
from .forms import AbonneForm, AbonnementForm, NewUserForm, AbonneProfilForm

import random

"""
class AbonneUpdateView(generic.UpdateView):
    form_class = AbonneProfilForm
    success_url = reverse_lazy('accueil')
    template_name = 'abonne/abonne_profil.html'

    # This keeps users from accessing the profile of other users.
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Abonne.objects.all()
        else:
            return Abonne.objects.filter(id=user.id)
"""


def abonne_creer(request):
	if request.method == 'POST':
		form = AbonneForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('accueil:index', args=())) 
		return render(request, 'abonne/abonne_creer.html', locals())
	form = AbonneForm()
	return render(request, 'abonne/abonne_creer.html', locals())


def abonne_lister(request):
	abonne_list = Abonne.objects.all().select_related('profil')
	return render(request, 'abonne/abonne_lister.html', {'abonne_list':abonne_list})


def abonnement(request):
	if request.method == 'POST':
		form = AbonnementForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('accueil:index', args=())) 
		return render(request, 'abonne/abonnement.html', locals())
	form = AbonnementForm()
	return render(request, 'abonne/abonnement.html', locals())


def abonnement_lister(request):
	abonnement_list = Abonnement.objects.all()


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		form1 = AbonneForm(request.POST)
		if form.is_valid() and form1.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			
			f = form1.save(commit=False)
			f.user = user
			f.matricule = user.username[:2] + str(Abonne.objects.count()+1).zfill(6)
			f.save()

			return redirect("accueil:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	form1 = AbonneForm()
	return render (request=request, template_name="abonne/register.html", context={
		"register_form":form, 'form1':form1})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("accueil:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="abonne/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	print("logout")
	return redirect("accueil:index")



