# from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
  path("cart", views.cart, name="cart"),
  path("payment", views.payment, name='payment'),
  path("products", views.products, name='products'),
  path("add-product", views.add_product, name='add_product'),
  path("add-to-cart/<int:product_id>", views.add_to_cart, name='add_to_cart'),
  path("edit-product/<int:product_id>", views.edit_product, name='edit_product'),
  path("delete-product/<int:product_id>", views.delete_product, name='delete_product'),
]