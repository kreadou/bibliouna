from rest_framework import serializers
from parametre.models import Soutenance

class SoutenanceSerializers(serializers.ModelSerializer):
	class Meta:
	    model = Soutenance
	    fields = ('id', 'description', 'designation', 'country', "taster_name", "title",
	    		'points', 'price', 'province', 'region', 'variety', 'winery')