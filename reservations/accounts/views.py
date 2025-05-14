from time import timezone
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.forms.UserSignUpForm import UserSignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from catalogue.models.cart import Cart, CartItem
from catalogue.models.price import Price
from catalogue.models.representation import Representation
from catalogue.models.representation_reservation import RepresentationReservation
from catalogue.models.reservation import Reservation
from catalogue.models.serializers import PriceSerializer, ReservationSerializer
from .forms import UserUpdateForm
from django.contrib.auth import logout
from accounts.forms.UserUpdateForm import UserUpdateForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from catalogue.models.user_meta import UserMeta
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password

class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("accounts:user-profile")
    template_name = "user/update.html"

    def test_func(self):
        pkInURL = self.kwargs['pk']
        return self.request.user.is_authenticated and self.request.user.id == pkInURL or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Vous n'avez pas l'autorisation d'accéder à cette page!")
        return redirect('accounts:user-profile')


class UserSignUpView(UserPassesTestMixin, CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def test_func(self):
        return self.request.user.is_anonymous or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Vous êtes déjà inscrit!")
        return redirect('home')


@login_required
def profile(request):
    languages = {
        "fr": "Français",
        "en": "English",
        "nl": "Nederlands",
    }

    return render(request, 'user/profile.html', {
        "user_language": languages[request.user.usermeta.langue],
    })


@login_required
def delete(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        user.delete()

        logout(request)
        return redirect('home')


def check_auth(request):
    return JsonResponse({"authenticated": True})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Nom d'utilisateur et mot de passe requis."}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_meta, _ = UserMeta.objects.get_or_create(user=user)
            user_meta.is_logged_in = True
            user_meta.active_token = token.key
            user_meta.save()

            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    
                }
            })
        else:
            return Response({"message": "Nom d'utilisateur ou mot de passe incorrect."}, status=401)

class LogoutView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            user_meta = UserMeta.objects.get(user=user)
            user_meta.is_logged_in = False
            user_meta.active_token = None
            user_meta.save()
            return Response({"message": "Déconnexion réussie."})
        return Response({"message": "Utilisateur non authentifié."}, status=401)

class UserMetaDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({"error": "Non autorisé."}, status=403)

        user_meta = get_object_or_404(UserMeta, user=request.user)
        return Response({
            "user": {
                "id": user_meta.user.id,
                "username": user_meta.user.username,
                "first_name": user_meta.user.first_name,
                "last_name": user_meta.user.last_name,
                "email": user_meta.user.email,
            },
            "is_logged_in": user_meta.is_logged_in,
        })
    

class UserCartView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
    # Vérifiez si l'utilisateur connecté correspond à l'ID utilisateur dans l'URL
        if request.user.id != user_id:
            return Response({"error": "Non autorisé."}, status=403)

        # Récupérez le panier de l'utilisateur
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            print(f"Aucun panier trouvé pour l'utilisateur {request.user.id}")
            return Response({"items": []})  # Panier vide si aucun panier n'existe

        # Construire la réponse avec les relations appropriées
        return Response({
            "id": cart.id,
            "items": [
                {
                    "id": item.id,
                    "title": item.representation.show.title,  # Titre du spectacle
                    "schedule": item.representation.schedule,  # Horaire
                    "location": item.representation.location.designation,  # Lieu
                    "quantity": item.quantity,  # Quantité
                    "price": {
                        "type": item.price.type,  # Type de billet
                        "amount": str(item.price.price),  # Prix du billet
                    },
                }
                for item in cart.items.select_related('representation__show', 'representation__location', 'price').all()
            ],
        })
        
    def post(self, request, user_id):
        try:
            data = request.data
            print(f"Données reçues : {data}")

            # Extraire les informations nécessaires
            representation_id = data.get('id')  # ID de la représentation
            quantities = data.get('quantities', [])  # Liste des quantités par type

            if not representation_id or not quantities:
                return Response({"error": "Données invalides. 'id' et 'quantities' sont requis."}, status=400)

            # Vérifier que la représentation existe
            representation = Representation.objects.filter(id=representation_id).first()
            if not representation:
                return Response({"error": f"Représentation introuvable pour l'ID {representation_id}."}, status=404)

            # Récupérez ou créez le panier de l'utilisateur
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Parcourez les quantités et ajoutez chaque type au panier
            for quantity in quantities:
                # Trouver le prix correspondant au type et au montant
                price = Price.objects.filter(type=quantity['type'], price=quantity['price']).first()
                if not price:
                    return Response({"error": f"Prix introuvable pour le type {quantity['type']} et le prix {quantity['price']}."}, status=400)

                # Ajouter ou mettre à jour l'article dans le panier
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    representation=representation,
                    price=price,  # Utiliser le champ price
                    defaults={'quantity': quantity['count']}
                )
                if not created:
                    cart_item.quantity += quantity['count']
                    cart_item.save()

            return Response({"message": "Articles ajoutés au panier avec succès !", "cart_id": cart.id})
        except Exception as e:
            print(f"Erreur : {e}")
            return Response({"error": str(e)}, status=400)

class UpdateCartItemView(APIView):
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        try:
            cart_item_id = request.data.get('cart_item_id')
            quantity = request.data.get('quantity')

            if not cart_item_id or quantity is None:
                return Response({"error": "Données invalides."}, status=400)

            # Vérifier que l'article appartient au panier de l'utilisateur
            cart_item = CartItem.objects.filter(id=cart_item_id, cart__user=request.user).first()
            if not cart_item:
                return Response({"error": "Article introuvable ou non autorisé."}, status=404)

            # Mettre à jour la quantité
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                # Supprimer l'article si la quantité est 0
                cart_item.delete()

            # Retourner le panier mis à jour
            cart = cart_item.cart
            items = cart.items.select_related('representation__show', 'price').all()
            cart_data = {
                "id": cart.id,
                "items": [
                    {
                        "id": item.id,
                        "title": item.representation.show.title,
                        "schedule": item.representation.schedule,
                        "location": item.representation.location.designation,
                        "price": {
                            "type": item.price.type,
                            "amount": str(item.price.price),
                        },
                        "quantity": item.quantity,
                    }
                    for item in items
                ],
            }
            return Response(cart_data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class DeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]

    def delete(self, request, user_id):
        try:
            cart_item_id = request.data.get('cart_item_id')

            if not cart_item_id:
                return Response({"error": "ID de l'article manquant."}, status=400)

            # Vérifier que l'article appartient au panier de l'utilisateur
            cart_item = CartItem.objects.filter(id=cart_item_id, cart__user=request.user).first()
            if not cart_item:
                return Response({"error": "Article introuvable ou non autorisé."}, status=404)

            # Supprimer l'article
            cart_item.delete()

            # Retourner le panier mis à jour
            cart = cart_item.cart
            items = cart.items.select_related('representation__show', 'price').all()
            cart_data = {
                "id": cart.id,
                "items": [
                    {
                        "id": item.id,
                        "title": item.representation.show.title,
                        "schedule": item.representation.schedule,
                        "location": item.representation.location.designation,
                        "price": {
                            "type": item.price.type,
                            "amount": str(item.price.price),
                        },
                        "quantity": item.quantity,
                    }
                    for item in items
                ],
            }
            return Response(cart_data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ClearCartView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart.items.all().delete()  # Supprimer tous les articles du panier
                print(f"Panier vidé pour l'utilisateur {request.user.id}")
                return JsonResponse({"message": "Panier vidé avec succès."}, status=200)
            else:
                return JsonResponse({"message": "Aucun panier trouvé."}, status=404)
        except Exception as e:
            print(f"Erreur lors de la suppression du panier : {str(e)}")
            return JsonResponse({"error": "Erreur lors de la suppression du panier."}, status=500)
        

class UserReservationsView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({"error": "Non autorisé."}, status=403)

        # Charger les relations nécessaires
        reservations = Reservation.objects.filter(user_id=user_id).prefetch_related(
            'representationreservation_set__price',
            'representationreservation_set__representation__show'
        ).order_by('-booking_date')

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

@login_required
def profile(request):
    languages = {
        "fr": "Français",
        "en": "English",
        "nl": "Nederlands",
    }

    return render(request, 'user/profile.html', {
        "user_language": languages[request.user.usermeta.langue],
    })


@login_required
def delete(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        user.delete()

        logout(request)
        return redirect('home')


def check_auth(request):
    return JsonResponse({"authenticated": True})


    
class PaymentSuccessView(APIView):
    authentication_classes = [TokenAuthentication]

    @transaction.atomic
    def post(self, request):
        data = request.data
        user = request.user
        quantities = data.get('quantities')  # Liste des quantités avec leurs détails (exemple : [{"representation_id": 2, "price_id": 1, "quantity": 2}, ...])

        if not quantities:
            return Response({"error": "Données manquantes."}, status=400)

        # Étape 1 : Créer une nouvelle réservation
        reservation = Reservation.objects.create(
            user=user,
            booking_date=timezone.now(),
            status="payée"  # Statut de la réservation
        )

        # Étape 2 : Créer les entrées dans RepresentationReservation
        for item in quantities:
            representation_id = item.get('representation_id')  # Récupérer le representation_id pour chaque élément
            price_id = item.get('price_id')
            quantity = item.get('quantity')

            if not representation_id or not price_id or not quantity:
                return Response({"error": "Données manquantes pour un des prix."}, status=400)

            # Vérifier si la représentation existe
            representation = Representation.objects.filter(id=representation_id).first()
            if not representation:
                return Response({"error": f"Représentation introuvable pour l'ID {representation_id}."}, status=404)

            # Vérifier si le prix existe
            price = Price.objects.filter(id=price_id).first()
            if not price:
                return Response({"error": f"Prix introuvable pour l'ID {price_id}."}, status=404)

            # Créer une entrée dans RepresentationReservation
            RepresentationReservation.objects.create(
                representation=representation,
                reservation=reservation,
                price=price,
                quantity=quantity
            )

        return Response({"message": "Paiement traité avec succès.", "reservation_id": reservation.id}, status=201)
    


class PriceListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        prices = Price.objects.all()
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data)
    


class RepresentationListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        if not title:
            return Response({"error": "Le titre est requis."}, status=400)

        representations = Representation.objects.filter(show__title__icontains=title)
        data = [
            {
                "id": representation.id,
                "show_id": representation.show.id,
                "location_id": representation.location.id,
                "schedule": representation.schedule,
            }
            for representation in representations
        ]
        return Response(data)
    

class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({"message": "Changez votre mot de passe."})
    

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({"error": "Ancien et nouveau mot de passe requis."}, status=400)

        if not user.check_password(old_password):
            return Response({"error": "L'ancien mot de passe est incorrect."}, status=400)

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": "Validation du mot de passe échouée.", "details": e.messages}, status=400)

        
        user.set_password(new_password)
        user.save()

        return Response({"message": "Mot de passe changé avec succès."}, status=200)
    


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        data = request.data

        # Update fields in the auth_user table (User model)
        if 'first_name' in data:
            request.user.first_name = data['first_name']
        if 'last_name' in data:
            request.user.last_name = data['last_name']
        if 'email' in data:
            request.user.email = data['email']

        # Save the updated user information
        request.user.save()

        return Response({
            "message": "Informations mises à jour avec succès.",
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        })