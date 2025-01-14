from django.contrib import admin
from .models import Artist, Locality, Location, Price, Reservation, Show, Type, ArtisteType, Representation, RepresentationReservation, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from catalogue.models import UserMeta

# Register your models here.
admin.site.register(Artist)
admin.site.register(Locality)
admin.site.register(Location)
admin.site.register(Price)
admin.site.register(Reservation)
admin.site.register(Show)
admin.site.register(Type)
admin.site.register(ArtisteType)
admin.site.register(Representation)
admin.site.register(RepresentationReservation)
admin.site.register(Review)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class UserMetaInline(admin.StackedInline):
    model = UserMeta
    can_delete = False
    verbose_name_plural = "user_meta"

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = [UserMetaInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
