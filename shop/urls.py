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
  path("table", views.product_table, name='product_table'),
  path("categories", views.all_categories, name='all_categories'),
  path("product-categories/<int:category_id>", views.categories, name='product-categories'),
  path("successful_payment", views.successful_payment, name='successful_payment'),
  path("checkout", views.checkout, name='checkout'),
  path("clear-cart", views.clear_cart, name='clear_cart'),
  path("remove-from-cart/<int:product_id>", views.remove_from_cart, name='remove_from_cart'),
]