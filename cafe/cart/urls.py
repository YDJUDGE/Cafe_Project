from django.urls import path
from .views import CartView, AddToCart, UpdateCartView

urlpatterns = [
    path('', CartView.as_view(), name="cart_view"),
    path('add/<int:product_pk>', AddToCart.as_view(), name="add_to_cart"),
    path('update/<int:product_pk>', UpdateCartView.as_view(), name="update_cart")
]

