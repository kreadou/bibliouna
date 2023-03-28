from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from parametre.models import Civilite, Profil
from django.utils import timezone


TYPES_ABONNES = (
    ('Etudiant', 'Etudiant'),
    ('Enseignant', 'Enseignant'),
    ('Autres', 'Autres'),
   )    

PERIODES_ABONNEMENTS = (
    ('Annuelle', 'Annuelle'),
    ('Semestrielle', 'Semestrielle'),
    ('Trimestrielle', 'Trimestrielle'),
    ('Mensuelle', 'Mensuelle'),
   )    

SEXES = (('M', 'Masculin'), ('F', 'Féminin'))


class Abonne(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="nom d'utilisateur")
    #profil = models.ForeignKey(Profil, on_delete=models.CASCADE, verbose_name="profil")
    
    type_abonne = models.CharField(max_length=15, choices=TYPES_ABONNES, default='Etudiant', verbose_name="type d'abonné")
    cellulaire = models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="cellulaire")
    matricule = models.CharField(max_length=15, default="", blank=True, null=True, verbose_name="matricule")
    
    class Meta:
        ordering = ('type_abonne',)

    def __str__(self):
        return "{0}".format(self.type_abonne)
        #return "{0}".format(self.profil.nom.upper()+' '+self.profil.prenoms.title())


class Abonnement(models.Model):
    abonne = models.ForeignKey(Abonne, on_delete=models.CASCADE, verbose_name="abonne")
    type_abonne = models.CharField(max_length=15, choices=TYPES_ABONNES, default='Etudiant', verbose_name="type d'abonné")
    periode_abonnement = models.CharField(max_length=15, choices=PERIODES_ABONNEMENTS, default='Annuelle', verbose_name="périodicité")
    date_debut = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date début")
    date_fin = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date fin")
    date_saisie = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date saisie")
    montant = models.IntegerField(default=0, blank=True, verbose_name="montant")
    regle = models.BooleanField(default=False, blank=True, verbose_name="reglé")
        
    class Meta:
        ordering = ('date_saisie',)

    def __str__(self):
        return "{0}".format(self.abonne, self.date_saisie)
