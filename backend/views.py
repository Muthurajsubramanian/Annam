from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from menu.models import MenuItem
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer, CheckoutSerializer


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail_view(request):
    """GET /api/orders/cart/ — current user's cart. Used to fill the floating cart badge."""
    cart = _get_or_create_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_add_view(request):
    """
    POST /api/orders/cart/add/
    body: { "menu_item": <id>, "quantity": 1 }
    Adds an item, or increases quantity if it's already in the cart.
    """
    cart = _get_or_create_cart(request.user)
    menu_item_id = request.data.get('menu_item')
    quantity = int(request.data.get('quantity', 1))

    try:
        menu_item = MenuItem.objects.get(pk=menu_item_id, is_active=True)
    except MenuItem.DoesNotExist:
        return Response({'detail': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

    item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        item.save()

    return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_view(request, item_id):
    """
    PATCH /api/orders/cart/items/<id>/  body: { "quantity": 2 }  — update quantity
    DELETE /api/orders/cart/items/<id>/                          — remove item
    """
    cart = _get_or_create_cart(request.user)
    try:
        item = cart.items.get(pk=item_id)
    except CartItem.DoesNotExist:
        return Response({'detail': 'Item not in cart.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        item.delete()
    else:
        quantity = int(request.data.get('quantity', item.quantity))
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_view(request):
    """
    POST /api/orders/checkout/
    body: { "delivery_address": "...", "phone": "..." }
    Converts the current cart into an Order (with snapshotted item prices/names)
    and empties the cart.
    """
    cart = _get_or_create_cart(request.user)
    if not cart.items.exists():
        return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CheckoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total=cart.total,
            delivery_address=serializer.validated_data.get('delivery_address', ''),
            phone=serializer.validated_data.get('phone', ''),
        )
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                item_name=cart_item.menu_item.name,
                unit_price=cart_item.menu_item.price,
                quantity=cart_item.quantity,
            )
        cart.items.all().delete()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list_view(request):
    """GET /api/orders/ — order history for the logged-in user."""
    orders = Order.objects.filter(user=request.user)
    return Response(OrderSerializer(orders, many=True).data)
