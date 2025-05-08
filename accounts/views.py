from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.forms.UserSignUpForm import UserSignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from catalogue.models.price import Price
from .forms import UserUpdateForm
from django.contrib.auth import logout
from accounts.forms.UserUpdateForm import UserUpdateForm
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from accounts.models.cart import Cart, CartItem
from catalogue.models.representation import Representation
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from accounts.models.cart import Cart

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


@login_required
def user_cart_template_view(request):
    # Vérifier si l'utilisateur a un panier
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        # Si aucun panier n'existe, afficher un message ou une page vide
        return render(request, 'user/user_cart.html', {'cart': None, 'message': "Votre panier est vide."})
    
    # Passer les données du panier au template
    return render(request, 'user/user_cart.html', {'cart': cart})


@receiver(post_save, sender=User)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.get_or_create(user=instance)

        
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
    
