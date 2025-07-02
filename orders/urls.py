from django.urls import path
from . import views 

urlpatterns = [
  path("orders", views.orders_table, name='orders_table'),

]