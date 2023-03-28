from django.db import models
from django.utils import timezone
from Utilitaire import dateAnglaisFrancais, iif
# START
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
# END

class Evenement(models.Model):
    TYPE_EVENEMENTS = (
    ('Actualité', 'Actualité'),
    ('Réunion', 'Réunion'),
    ("Rencontre", "Rencontre"),
  )  

    type_evenement = models.CharField(max_length=255, choices=TYPE_EVENEMENTS, blank=True, verbose_name="type d'évènement")
    titre = models.CharField(max_length=255, blank=True, verbose_name="titre de l'évènement")
    date_du = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="du")
    date_au = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="au")
    date_publication = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date publication")
    lieu = models.CharField(max_length=255, blank=True, verbose_name="lieu")
    resume = models.TextField(default="", blank=True, null=True, verbose_name="résumé")
    photo = models.ImageField(upload_to='images/evenements', blank=True, null=True, verbose_name="photo evènement")
    
    photo_middle = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(400, 240)],
                                     format='JPEG',
                                     options={'quality': 60})

    photo_medium = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(250, 150)],
                                     format='JPEG',
                                     options={'quality': 60})
    
    photo_small = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    def __str__(self):
        return "{0}, {1}".format(self.titre, dateAnglaisFrancais(self.date_du)) 


class DocumentEvenement(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, blank=True, null=True, verbose_name="evènement")
    photo = models.FileField(upload_to='images/evenements', blank=True, null=True, verbose_name="photo")
    fichier = models.FileField(upload_to='fichier/evenements', blank=True, null=True, verbose_name="vidéo / autres fichiers")
   
    
    photo_middle = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(400, 240)],
                                     format='JPEG',
                                     options={'quality': 60})

    photo_medium = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(250, 150)],
                                     format='JPEG',
                                     options={'quality': 60})
    
    photo_small = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})
    
    def __str__(self):
        return "{0}".format(self.evenement)


