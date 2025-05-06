from rest_framework import serializers
from accounts.models.cart import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    representation_title = serializers.CharField(source='representation.show.title')
    representation_schedule = serializers.DateTimeField(source='representation.schedule')
    representation_location = serializers.CharField(source='representation.location.designation')
    price_type = serializers.CharField(source='price.type')
    price_amount = serializers.DecimalField(source='price.price', max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['id', 'representation_title', 'representation_schedule', 'representation_location', 'quantity', 'price_type', 'price_amount']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()