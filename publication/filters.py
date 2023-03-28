import django_filters 
from django_filters import CharFilter

from parametre.models import Soutenance, Ouvrage, Article


class SoutenanceFilter(django_filters.FilterSet):
	titre = CharFilter(field_name="titre", lookup_expr='icontains')
	class Meta:
		model = Soutenance
		fields = ['titre', 'auteur', 'specialite', 'motcles', 'resume']