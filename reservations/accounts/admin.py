from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from catalogue.models.cart import Cart, CartItem
from catalogue.models.price import Price
from catalogue.models.representation import Representation
from catalogue.models.reservation import Reservation
from catalogue.models import ArtistType, Show, Review
from catalogue.models.representation_reservation import RepresentationReservation
from catalogue.models.artist_show import ArtistShow

# Unregister the default User model
admin.site.unregister(User)

# Register the User model with your custom UserAdmin
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

@admin.register(ArtistType)
class ArtistTypeAdmin(admin.ModelAdmin):
    list_display = ('artist', 'type')
    list_filter = ('type',)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'stars', 'review')
    list_filter = ('stars',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'representation', 'price', 'quantity')
    list_filter = ('price__type',)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('type', 'price')
    search_fields = ('type',)

@admin.register(Representation)
class RepresentationAdmin(admin.ModelAdmin):
    list_display = ('show', 'schedule', 'location')
    list_filter = ('location',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)

@admin.register(RepresentationReservation)
class RepresentationReservationAdmin(admin.ModelAdmin):
    list_display = ('representation', 'reservation', 'price', 'quantity')
    list_filter = ('representation', 'price')
    search_fields = ('reservation__user__username', 'representation__show__title')

@admin.register(ArtistShow)
class ArtistShowAdmin(admin.ModelAdmin):
    list_display = ('artist', 'show')
    list_filter = ('artist', 'show')
    search_fields = ('artist__firstname', 'artist__lastname', 'show__title')