from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('bibliouna', TemplateView())
    path('administration/', include('administration.urls')),
	path('galerie/', include('galerie.urls')),
    path('actualite/', include('actualite.urls')),
    path('abonne/', include('abonne.urls')),
	path('publication/', include('publication.urls')),
	path('', include('accueil.urls')),
	path('parametre/', include('parametre.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
