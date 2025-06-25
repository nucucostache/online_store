from django.shortcuts import render


def cart(request):
    return render(request, 'shop/cart.html')

def payment(request):
    return render(request, 'shop/payment.html')

