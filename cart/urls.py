from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-placed/', views.order_placed, name='order_placed'),
    path('add-to-cart/', views.add_product_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_product_from_cart, name='remove_from_cart'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('update-cart/', views.update_cart, name='update_cart'),  # Added update cart URL
]
