from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='menu_item.name', read_only=True)
    price = serializers.DecimalField(source='menu_item.price', max_digits=8, decimal_places=2, read_only=True)
    image_url = serializers.URLField(source='menu_item.image_url', read_only=True)
    subtotal = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'name', 'price', 'image_url', 'quantity', 'subtotal']
        extra_kwargs = {'menu_item': {'write_only': True}}


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'item_count']


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'item_name', 'unit_price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'delivery_address', 'phone', 'created_at', 'items']
        read_only_fields = ['id', 'status', 'total', 'created_at', 'items']


class CheckoutSerializer(serializers.Serializer):
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
