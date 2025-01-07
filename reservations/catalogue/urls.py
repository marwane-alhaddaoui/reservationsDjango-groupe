"""reservations.catalogue URL Configuration
"""
from django.urls import path, include
from . import views
from django.contrib import admin
from .models import Artist

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

]

admin.site.index_title = "Projet Réservations"
admin.site.index_header = "Projet Réservations HEADER"
admin.site.site_title = "Spectacles"
