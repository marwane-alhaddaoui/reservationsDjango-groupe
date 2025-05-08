from django.urls import path
from .views import ClearCartView, DeleteCartItemView, UpdateCartItemView, UserCartView, UserSignUpView, profile, UserUpdateView, delete, user_cart_template_view

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('profile/', profile, name='user-profile'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('profile/delete/<int:pk>/', delete, name='user-delete'),
    path('user-cart/', user_cart_template_view, name='user-cart-template'),

    path('api/user-cart/<int:user_id>/', UserCartView.as_view(), name='user-cart'), 
    path('api/clear-cart/', ClearCartView.as_view(), name='clear-cart'),
    path('api/user-cart/delete/<int:user_id>/', DeleteCartItemView.as_view(), name='delete-cart-item'),
    path('api/user-cart/update/', UpdateCartItemView.as_view(), name='update-cart-item'), 
    
    

]
