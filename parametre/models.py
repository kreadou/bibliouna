from django.db import models
from django.contrib.auth.models import User
from Utilitaire import dateAnglaisFrancais, iif
from multipleselectionfield import MultipleSelectionField
from django.utils import timezone
import datetime

LANGUES_PUBLICATIONS = (
    ('Français', 'Français'),
    ('Anglais', 'Anglais'),
    ('Autres', 'Autres'),
   )    

FORMATS_ELECTRONIQUES = (
    ('texte', 'texte'),
    ('pdf', 'pdf'),
    ('audio', 'audio'),
    ('vidéo', 'vidéo'),
   )    

TYPES_PUBLICATIONS = (
    ('ouvrage', 'ouvrage'),
    ('thèse', 'thèse'),
    ('mémoire', 'mémoire'),
    ('article', 'article'),
   )    


UFRS = (
    ('SFA - Sciences Fondamentales et Appliquées', 'SFA - Sciences Fondamentales et Appliquées'),
    ('SN - Sciences de la Nature', 'SN - Sciences de la Nature'),
    ('STA - Sciences et Technologies Alimentaires', 'STA - Sciences et Technologies Alimentaires'),
    ("SGE - Sciences et Gestion de l'Environnement", "SGE - Sciences et Gestion de l'Environnement"),
    ("EPSS - Ecole Préparatoire aux Sciences de la Santé", "EPSS - Ecole Préparatoire aux Sciences de la Santé"),
    ("CFC - Centre de Formation Continue", "CFC - Centre de Formation Continue"),

   )  

SPECIALITES = [
    ('Mathématiques', 'Mathématiques'),
    ('Informatique', 'Informatique'),
    ('Physique', 'Physique'),
    ('Chimie', 'Chimie'),
    ('Biologie', 'Biologie'),
    ('Dictoinnaire', 'Dictionnaire'),
    ('Electronique', 'Electronique'),
    ('Médecine', 'Médecine'),
    ('Zoologie', 'Zoologie'),
    ('Biochimie', 'Biochimie'),
    ('Biosciences', 'Biosciences'),
    ('Agriculture', 'Agriculture'),
    ('Sciences Sociales', 'Sciences Sociales'),
    ('Droit', 'Droit'),
    ('Géologie', 'Géologie'),
    ('Environnement', 'Environnement'),
    ('Gestion et Economie', 'Gestion et Economie'),
]
SPECIALITES.sort()

DISCIPLINES = [
    ('Mathématiques', 'Mathématiques'),
    ('Informatique', 'Informatique'),
    ('Physique', 'Physique'),
    ('Chimie', 'Chimie'),
    ('Biologie', 'Biologie'),
    ('Dictoinnaire', 'Dictionnaire'),
    ('Electronique', 'Electronique'),
    ('Médecine', 'Médecine'),
    ('Zoologie', 'Zoologie'),
    ('Biochimie', 'Biochimie'),
    ('Biosciences', 'Biosciences'),
    ('Agriculture', 'Agriculture'),
    ('Sciences Sociales', 'Sciences Sociales'),
    ('Droit', 'Droit'),
    ('Géologie', 'Géologie'),
    ('Environnement', 'Environnement'),
    ('Gestion et Economie', 'Gestion et Economie'),
]
DISCIPLINES.sort()


LABORATOIRES_RECHERCHES = (
    ("01", "SGE - Laboratoire des Sciences de l'Environnement"),
    ("02", 'LGE - Laboratoire Géosciences et Environnement'),
    ("03", "LEBA - Laboratoire d'Environnement et de Biologie Aquatique"),
    ("04", "LBATPT - Laboratoire de Biochimie Alimentaire et Technologies des Produits Tropicaux"),
    ("05", "LNSA - Laboratoire de Nutrition et Sécurité Alimentaire"),
    ("06", "LBMA - Laboratoire de Biotechnologie et Microbiologie des Aliments"),
    ("07", "LBB - Laboratoire de Biocatalyse et des Bioprocédés"),
   )  


QUALIFICATIONS = (
    ("Enseignant", 'Enseignant'),
    ("Professeur", 'Professeur'),
    ("Maître de Conférence", 'Maître de Conférence'),
    ("Professeur Titulaire", "Professeur Titulaire"),
    ("Enseignant-Chercheur", 'Enseignant-Chercheur'),
    ("Non renseignée", 'Non renseignée'),
  )  


TITRES = (
    ('Président', 'Président'),
    ('Directeur', 'Directeur'),
    ('Co-Directeur', 'Co-Directeur'),
    ("Rapporteur", "Rapporteur"),
    ("Examinateur", "Examinateur"),
    ("Coordinateur", "Coordinateur"),
    ("Evaluateur", "Evaluateur"),
  )  


STATUTS = (
    ('Président', 'Président'),
    ('Directeur', 'Directeur'),
    ('Co-Directeur', 'Co-Directeur'),
    ("Rapporteur", "Rapporteur"),
    ("Examinateur", "Examinateur"),
    ("Coordinateur", "Coordinateur"),
    ("Evaluateur", "Evaluateur"),
  )  


CIVILITES = (
    ('Monsieur', 'M.'),
    ('Madame', 'Mme'),
    ('Mademoiselle', 'Mlle'),
  )  

ETABLISSEMENTS = (
    ("Université Nangui Abrogoua de Côte d'Ivoire", "Université Nagui Abrogoua de Côte d'Ivoire"),
    ("Université Félix Houphouet Boigny de Côte d'Ivoire", "Université Félix Houphouet Boigny de Côte d'Ivoire"),
    ("Université Alassane Ouattara de Bouaké", "Université Alassane Ouattara de Bouaké"),
    ("Université Jean Lourougnon Guédé de Daloa (Côte d'Ivoire)", "Université Jean Lourougnon Guédé de Daloa (Côte d'Ivoire)"),
    ("Université de Man (Côte d'Ivoire)", "Université de Man (Côte d'Ivoire)"),
  )  


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Continent(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Pays(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, verbose_name="Continent")
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")
    abrege = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="Abrégé")
    
    class Meta:
        ordering=('libelle',)   
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Region(models.Model):
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="Pays")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)    
    def __str__(self):
        return "{0}".format(self.libelle)

class Departement(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Région")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)    

    def __str__(self):
        return "{0}".format(self.libelle)

class Ville(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    class Meta:
        ordering=('libelle',)    
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Commune(models.Model):
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, verbose_name="Ville")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)

class Civilite(models.Model):
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    abrege = models.CharField(max_length=255, default="", blank=True,  null=True, verbose_name=u"Abrégé")

    def __str__(self):
        return "{0}".format(self.abrege)

class Fonction(models.Model):
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Profession(models.Model):
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Service(models.Model):
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé")

    def __str__(self):
        return "{0}".format(self.libelle)

class TypeActivite(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")
    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)

class Activite(models.Model):
    typeActivite = models.ForeignKey(TypeActivite, on_delete=models.CASCADE, verbose_name="Type d'activite")
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")

    def __str__(self):
        return "{0}".format(self.libelle)


class Profil(models.Model):
    SEXES = (('M', 'Masculin'), ('F', 'Féminin'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="nom d'utilisateur") # La liaison OneToOne vers le modèle User
    civilite = models.CharField(max_length=20, choices=CIVILITES, blank=True, verbose_name="civilité")
    nom = models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="nom")
    prenoms = models.CharField(max_length=100, default="", blank=True, null=True, verbose_name="prenoms")
    fonction = models.ForeignKey(Fonction, on_delete=models.CASCADE, verbose_name="fonction")
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, verbose_name="profession")
    telephone = models.CharField(max_length=20, default="", blank=True, null=True, verbose_name="téléphone")
    cellulaire = models.CharField(max_length=20, default="", blank=True, null=True, verbose_name="cellulaire")
    email = models.CharField(max_length=100, default="", blank=True, null=True, verbose_name="e-mail")
    sexe = models.CharField(max_length=1, choices=SEXES, default='M', verbose_name="sexe")
    photo = models.ImageField(upload_to='users', blank=True, null=True, verbose_name="photo")
    
    def __str__(self):
        if self.user.first_name:
            return "{0}, {1}".format(self.user.last_name.upper()+' '+self.user.first_name.title(), self.fonction)
        else:
            return "{0}, {1}".format(self.user.last_name.upper(), self.fonction)

class Categorie(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return u"{0}".format(self.libelle)


class Qualification(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)

class Statut(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="Libellé")
    
    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)

class Discipline(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="Libellé")
    #abrege = models.CharField(max_length=255, default="", blank=True,  null=True, verbose_name="Abrégé")

    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)

class Titre(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    abrege = models.CharField(max_length=255, default="", blank=True, verbose_name="Aabrégé")
    class Meta:
        ordering = ('libelle',)
   
    def __str__(self):
        return self.libelle

class Ufr(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    abrege = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="abrégé")
    class Meta:
        ordering = ('libelle',)
   
    def __str__(self):
        return self.libelle

class Specialite(models.Model):
    libelle = models.CharField(max_length=255, default="", unique=True, verbose_name="spécialité")
    #abrege = models.CharField(max_length=255, default="", blank=True, verbose_name="abrégé")
    class Meta:
        pass#"ordering = ('libelle',)
   
    def __str__(self):
        return self.libelle

class Laboratoire(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    abrege = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="abrégé")
    class Meta:
        ordering = ('libelle',)
   
    def __str__(self):
        return self.libelle

class Etablissement(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    abrege = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="abrégé")
    class Meta:
        ordering = ('libelle',)
   
    def __str__(self):
        return self.libelle

class Motcle(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    class Meta:
        ordering = ('libelle',)
   
    def __str__(self):
        return self.libelle

class Editeur(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Raison sociale")
    telephone = models.CharField(max_length=20, default="", blank=True, null=True, verbose_name="téléphone")
    photo = models.ImageField(upload_to='editeurs', blank=True, null=True, verbose_name="photo maison d'édition")
    
    class Meta:
        ordering = ('nom',)

    def __str__(self):
        return self.nom.upper()

class Auteur(models.Model):
    nom = models.CharField(max_length=255, verbose_name="nom")
    prenoms = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="prénoms")
    photo = models.ImageField(upload_to='auteurs', blank=True, null=True, verbose_name="photo de l'auteur")
    class Meta:
        ordering = ('nom', 'prenoms')    

    def __str__(self):
        return self.nom.upper()

class Ouvrage(models.Model):
    titre = models.CharField(max_length=255, verbose_name="titre")
    titre_parallele = models.CharField(max_length=255, default="", blank=True, verbose_name="titre parallèle")
    sous_titre = models.CharField(max_length=255, default="", blank=True, verbose_name="sous titre")  
    annee = models.SmallIntegerField(default=1975, blank=True, verbose_name="année")
    isbn = models.CharField(max_length=20, blank=True, verbose_name="iSBN*")
    cote = models.CharField(max_length=255, default="", blank=True, verbose_name="côte ou indexation")
    note = models.CharField(max_length=255, default="", blank=True, verbose_name="note générale")
    resume = models.TextField(default="", blank=True, verbose_name="résumé")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="discipline")

    langue_publication = MultipleSelectionField(max_length=255, default="Français", blank=True, choices=LANGUES_PUBLICATIONS, verbose_name="langues publications")
    langue_originale = MultipleSelectionField(max_length=255, default="Français", blank=True, choices=LANGUES_PUBLICATIONS, verbose_name="langues originales")
    url_associe = models.CharField(max_length=20, default="", blank=True, verbose_name="url associé")
    format_electronique = MultipleSelectionField(max_length=255, default="texte", blank=True, null=True, choices=FORMATS_ELECTRONIQUES, verbose_name="formats électroniques")
    type_publication = models.CharField(max_length=255, default='ouvrage', choices=TYPES_PUBLICATIONS, verbose_name="type de publication")

    editeurs = models.ManyToManyField(Editeur, blank=True)
    auteurs = models.ManyToManyField(Auteur, blank=True)
    motcles = models.ManyToManyField(Motcle, blank=True, verbose_name="Mots-clés")
    photo = models.ImageField(upload_to='ouvrages', blank=True, null=True, verbose_name="photo couverture")
    
    fpdf = models.FileField(upload_to='fpdfs', blank=True, null=True, verbose_name="fichier en pdf")
    ftexte = models.FileField(upload_to='ftextes', blank=True, null=True, verbose_name="fichier en texte")
    faudio = models.FileField(upload_to='faudios', blank=True, null=True, verbose_name="fichier en audio")
    fvideo = models.FileField(upload_to='fideos', blank=True, null=True, verbose_name="fichier en vidéo")

    valide_saisie = models.BooleanField(default=False, blank=True, verbose_name="validé la saisie")
    
    def __str__(self):
        return '{0}, {1}'.format(self.titre, self.type_publication)

class Membre(models.Model):
    nom = models.CharField(max_length=150, unique=True, verbose_name="nom & prénoms")
    qualification = models.ForeignKey(Qualification, default=1, on_delete=models.CASCADE, verbose_name="qualification")

    class Meta:
        ordering = ['nom']

    def __str__(self):
        try:
            return '{} - [{}]'.format(self.nom.upper(), self.qualification)
        except:
            return self.nom.title()

class Soutenance(models.Model):
    titre = models.TextField(verbose_name="titre")
    auteur = models.CharField(max_length=255, blank=True, verbose_name="auteur")
    #directeur = models.CharField(max_length=255, blank=True, verbose_name="directeur")
    #co_directeur = models.CharField(max_length=255, default="", blank=True, verbose_name="co-directeur")
    ufr = models.ForeignKey(Ufr, on_delete=models.CASCADE, verbose_name="ufr", blank=True, null=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, blank=True, null=True, verbose_name="spécialité")
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE, blank=True, null=True, verbose_name="laboratoire")
    
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, verbose_name="université / établissement")
    
    date_soutenance = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date de soutenance")
    
    annee_soutenance = models.CharField(max_length=4, default="", blank=True, null=True, verbose_name="année de soutenance")

    #issn = models.CharField(max_length=255, default="", blank=True, verbose_name="issn")
    cote = models.CharField(max_length=255, blank=True, verbose_name="côte ou indexation")
    #discipline = models.CharField(max_length=255, choices=DISCIPLINES, verbose_name="discipline")
    note_generale = models.CharField(max_length=255, blank=True, verbose_name="note générale")
    resume = models.TextField(default="", blank=True, verbose_name="résumé")
    langue_publication = MultipleSelectionField(max_length=255, default="Français", blank=True, choices=LANGUES_PUBLICATIONS, verbose_name="langues publications")
    langue_originale = MultipleSelectionField(max_length=255, default="Français", blank=True, choices=LANGUES_PUBLICATIONS, verbose_name="langues originales")
    url_associe = models.CharField(max_length=20, blank=True, verbose_name="url associé")
    format_electronique = MultipleSelectionField(max_length=255, default="pdf", blank=True, choices=FORMATS_ELECTRONIQUES, verbose_name="formats électroniques")

    type_publication = models.CharField(max_length=255, default='thèse', choices=TYPES_PUBLICATIONS, verbose_name="type de publication")
    photo = models.ImageField(upload_to='theses', blank=True, null=True, verbose_name="photo couverture")
    fpdf = models.FileField(upload_to='fpdfs', blank=True, null=True, verbose_name="fichier en pdf")
    ftexte = models.FileField(upload_to='ftextes', blank=True, null=True, verbose_name="fichier en texte")
    faudio = models.FileField(upload_to='faudios', blank=True, null=True, verbose_name="fichier en audio")
    fvideo = models.FileField(upload_to='fideos', blank=True, null=True, verbose_name="fichier en vidéo")
    motcles = models.ManyToManyField(Motcle, blank=True, verbose_name="Mots-clés")
    valide_saisie = models.BooleanField(default=False, blank=True, verbose_name="validé la saisie")
    membres = models.ManyToManyField(Membre, through='Jury', verbose_name="membres du jury")

    def __str__(self):
        return "{0}, {1}".format(self.titre, self.auteur)

class Jury(models.Model):
    soutenance = models.ForeignKey(Soutenance, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    statuto  = models.CharField(max_length=255, choices=STATUTS, blank=True, verbose_name="statut")
    statut = models.ForeignKey(Statut, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = (('soutenance', 'membre'),)

    def __str__(self):
        return '{0}, {1} {2}'.format(self.soutenance, self.membre, self.statut)

class Article(TimeStampModel):
    titre = models.TextField(verbose_name="titre")
    auteur = models.CharField(max_length=255, blank=True, verbose_name="auteur")
    directeur = models.CharField(max_length=255, blank=True, verbose_name="directeur")
    co_directeur = models.CharField(max_length=255, default="", blank=True, verbose_name="co-directeur")
    
    ufr = models.ForeignKey(Ufr, on_delete=models.CASCADE, verbose_name="ufr", blank=True, null=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, blank=True, null=True, verbose_name="spécialité")
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE, blank=True, null=True, verbose_name="laboratoire")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, blank=True, null=True, verbose_name="discipline")

    date_parution = models.DateField(default=timezone.now, blank=True, verbose_name="date parution")
    issn = models.CharField(max_length=255, default="", blank=True, verbose_name="issn")
    cote = models.CharField(max_length=255, blank=True, verbose_name="côte ou indexation")
    
    note_generale = models.CharField(max_length=255, blank=True, verbose_name="note générale")
    resume = models.TextField(default="", blank=True, verbose_name="résumé")
    langue_publication = MultipleSelectionField(max_length=255, default="Français", blank=True, choices=LANGUES_PUBLICATIONS, verbose_name="langues publications")
    langue_originale = MultipleSelectionField(max_length=255, default="Français", blank=True, choices=LANGUES_PUBLICATIONS, verbose_name="langues originales")
    url_associe = models.CharField(max_length=20, blank=True, verbose_name="url associé")
    format_electronique = MultipleSelectionField(max_length=255, default="texte", blank=True, choices=FORMATS_ELECTRONIQUES, verbose_name="formats électroniques")

    type_publication = models.CharField(max_length=255, default='article', choices=TYPES_PUBLICATIONS, verbose_name="type de publication")
    photo = models.ImageField(upload_to='articles', blank=True, null=True, verbose_name="photo couverture")
   
    fpdf = models.FileField(upload_to='fpdfs', blank=True, null=True, verbose_name="fichier en pdf")
    ftexte = models.FileField(upload_to='ftextes', blank=True, null=True, verbose_name="fichier en texte")
    faudio = models.FileField(upload_to='faudios', blank=True, null=True, verbose_name="fichier en audio")
    fvideo = models.FileField(upload_to='fideos', blank=True, null=True, verbose_name="fichier en vidéo")

    valide_saisie = models.BooleanField(default=False, blank=True, verbose_name="validé la saisie")

    def __str__(self):
        return '{0}, {1}'.format(self.type_publication, self.titre)

class Societe(models.Model):
    raisonSociale = models.CharField(max_length=255, verbose_name="raison sociale")
    sigle = models.CharField(max_length=50, default="", blank=True,  null=True, verbose_name="sigle")
    telephone = models.CharField(max_length=20, default="", blank=True,  null=True, verbose_name="téléphone")
    cellulaire = models.CharField(max_length=20, default="", blank=True,  null=True, verbose_name="cellulaire")
    pagination = models.PositiveIntegerField(default=5, blank=True, verbose_name="nombre de ligne des tableaux")
    photo = models.ImageField(upload_to='images', default="", blank=True, null=True, verbose_name="photo")
    logo = models.ImageField(upload_to='images', default="", blank=True, null=True, verbose_name="logo")
    email = models.EmailField(default="", blank=True, null=True, verbose_name="e-mail")
    alerte_email_jour = models.PositiveIntegerField(default=5, blank=True,  null=True, verbose_name="alerte email (en jours)")
    dateEnvoiEmail = models.DateField(default=timezone.now, blank=True,  null=True, verbose_name="date envoi des email")
    envoiEmailEffectue = models.BooleanField(default=False, verbose_name="envoi de mail effectué")
    nbreJourMaxDateEcheance = models.SmallIntegerField(default=90, blank=True,  null=True, verbose_name="nombre de jours max avant échéance")
    entete_table = models.BooleanField(default=False, verbose_name="entêtes des tableaux en couleur des apps")
    
    def __str__(self):
        return "{0}".format(self.raisonSociale)


class Partenaire(models.Model):
    raisonSociale = models.CharField(max_length=255, verbose_name="raison sociale")
    sigle = models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="sigle")
    telephone = models.CharField(max_length=20, default="", blank=True, null=True, verbose_name="téléphone")
    cellulaire = models.CharField(max_length=20, default="", blank=True, null=True, verbose_name="cellulaire")
    email = models.EmailField(default="", blank=True, null=True, verbose_name="e-mail")
    logo = models.ImageField(upload_to='partenaires', default="", blank=True, null=True, verbose_name="logo")
    siteweb = models.CharField(max_length=200, default="", blank=True, null=True, verbose_name="site web")

    def __str__(self):
        return "{0}".format(self.raisonSociale)


class Contact(models.Model):
    nom = models.CharField(max_length=255, verbose_name="nom")
    prenoms = models.CharField(max_length=255, verbose_name="prénoms")
    telephone = models.CharField(max_length=20, default="", blank=True,  null=True, verbose_name="téléphone")
    email = models.EmailField(default="", blank=True, null=True, verbose_name="e-mail")
    sujet = models.TextField(default="", blank=True, null=True, verbose_name="sujet")
    date_contact = models.DateField(default=timezone.now, blank=True, verbose_name="date contact")
    lu = models.BooleanField(default=False, blank=True, verbose_name="message lu")

    def __str__(self):
        return "{0}".format(self.nom.upper()+' '+self.prenoms.title())
