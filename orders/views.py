from django.shortcuts import render
from .models import Order


def orders_table(request):
    ordersFromDb = Order.objects.all()
    return render(request, 'orders/orders_table.html', {'list_orders': ordersFromDb})


