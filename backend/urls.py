from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail_view, name='cart-detail'),
    path('cart/add/', views.cart_add_view, name='cart-add'),
    path('cart/items/<int:item_id>/', views.cart_item_view, name='cart-item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('', views.order_list_view, name='order-list'),
]
