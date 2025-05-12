"""reservations.catalogue URL Configuration
"""
from django.urls import path, include
from . import views
from django.contrib import admin
from .models import Artist
from api.catalogue.views import ArtistListCreateView, ArtistRetrieveUpdateDestroyView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'catalogue'

urlpatterns = [

    path('artist/', views.artist.index, name='artist-index'),
    path('artist/<int:artist_id>', views.artist.show, name='artist-show'),
    path('artist/edit/<int:artist_id>', views.artist.edit, name='artist-edit'),
    path('artist/create', views.artist.create, name='artist-create'),
    path(
        'artist/delete/<int:artist_id>/',
        views.artist.delete,
        name='artist-delete'),
    path('admin/', admin.site.urls),
    path('type/', views.type.index, name='type-index'),
    path('type/<int:type_id>', views.type.show, name='type-show'),
        path('locality/', views.locality.index, name='locality-index'),
    path('locality/<int:locality_id>', views.locality.show, name='locality-show'),
    path('price/', views.price.index, name='price-index'),
    path('price/<int:price_id>', views.price.show, name='price-show'),
    path('location/', views.location.index, name='location-index'),
    path('location/<int:location_id>', views.location.show, name='location-show'),
        path('show/', views.show_.index, name='show-index'),
    path('show/<int:show_id>', views.show_.show, name='show-show'),
        path('representation/', views.representation.index, name='representation-index'),
    path('representation/<int:representation_id>', views.representation.show, name='representation-show'),
    
path('api/artists/', ArtistListCreateView.as_view(), name='artist-list'),
path('api/artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),

path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),






]

admin.site.index_title = "Projet Réservations"
admin.site.index_header = "Projet Réservations HEADER"
admin.site.site_title = "Spectacles"
