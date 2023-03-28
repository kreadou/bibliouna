# -*- coding:utf-8 -*-
from django.contrib import admin
from parametre.models import *

admin.site.register(Continent)
admin.site.register(Pays)
admin.site.register(Region)
admin.site.register(Departement)
admin.site.register(Ville)
admin.site.register(Commune)
admin.site.register(Fonction)
admin.site.register(Profession)
admin.site.register(Service)
admin.site.register(TypeActivite)
admin.site.register(Activite)
admin.site.register(Profil)
admin.site.register(Societe)
admin.site.register(Categorie)
admin.site.register(Discipline)
admin.site.register(Civilite)
admin.site.register(Specialite)
admin.site.register(Ouvrage)
#admin.site.register(Soutenance)
admin.site.register(Article)
admin.site.register(Auteur)
admin.site.register(Editeur)
admin.site.register(Motcle)
admin.site.register(Jury)
admin.site.register(Membre)
admin.site.register(Qualification)


admin.site.register(Ufr)
admin.site.register(Etablissement)
admin.site.register(Laboratoire)

admin.site.register(Partenaire)
admin.site.register(Contact)


class JuryInline(admin.TabularInline):
    model = Jury
    extra = 1

class SoutenanceAdmin(admin.ModelAdmin):
    inlines = (JuryInline,)
    list_display = ['titre', 'auteur', 'specialite',]
    list_filter = ('specialite',)
    search_fields = ['auteur__icontains',]

admin.site.register(Soutenance, SoutenanceAdmin)