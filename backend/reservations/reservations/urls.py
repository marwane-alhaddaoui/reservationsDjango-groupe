# backend/reservations/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from accounts.views import MyTokenObtainPairView  
from rest_framework_simplejwt.views import TokenRefreshView
from api.accounts.api_views import RegisterAPI
from api.profile import profile_view

urlpatterns = [
    # Page d’accueil classique (template home.html)
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Authentification Django « classique » (login, logout, password reset)
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # URLs de l’app « catalogue » (front office)
    path('catalogue/', include('catalogue.urls')),

    # Admin site et password reset
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_complete",
    ),
    path('admin/', admin.site.urls),

    # === API REST (JWT + inscr./profils + catalogue) ===

    # 1) Obtenir un couple (refresh, access)
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
# 2) Rafraîchir l’access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 3) S’inscrire (via ta classe DRF RegisterAPI)
    path('api/register/', RegisterAPI.as_view(), name='register'),
    # 4) Liste et création d’artistes (GET POST)
    path('api/artists/', include('catalogue.api_urls')),
    # 5) Infos du profil de l’utilisateur connecté
    path('api/profile/', profile_view, name='api-profile'),
]

# Personnalisation du header/footer de l’admin
admin.site.index_title = "Projet Réservations"
admin.site.index_header = "Projet Réservations HEADER"
admin.site.site_title = "Spectacles"
