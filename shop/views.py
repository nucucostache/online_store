from django.shortcuts import redirect, render
from shop.forms import ProductForm
from .models import Product

def cart(request):
    lista_mea = Product.objects.all()
    # lista_mea = Product.objects.filter(title__icontains='Mouse')
    # lista_mea = [
    #     Product.objects.get(title='Mouse')
    # ]
    # print(lista_mea[0].thumbnail)
    # lista_mea = [
    #     {
    #         'id': 1, 
    #         'title': 'Wireless Bluetooth Headphones', 
    #         'description': 'High-quality wireless headphones with noise cancellation',
    #         'price': 99.99, 
    #         'stock': 15,
    #         'made_in': 'Germany',
    #         'quantity': 2
    #     },
    #     {
    #         'id': 2, 
    #         'title': 'Protective Smartphone Case', 
    #         'description': 'Durable case with shock absorption for all smartphone models',
    #         'price': 24.99, 
    #         'stock': 50,
    #         'made_in': 'China',
    #         'quantity': 1
    #     },
    #     {
    #         'id': 3, 
    #         'title': 'Portable Bluetooth Speaker', 
    #         'description': 'Compact speaker with 12-hour battery life and waterproof design',
    #         'price': 79.99, 
    #         'stock': 8,
    #         'made_in': 'Japan',
    #         'quantity': 1
    #     },
    #     {
    #         'id': 4, 
    #         'title': 'USB-C Charging Cable', 
    #         'description': 'Fast charging cable compatible with most modern devices',
    #         'price': 12.99, 
    #         'stock': 100,
    #         'made_in': 'Taiwan',
    #         'quantity': 3
    #     },
    #     {
    #         'id': 5, 
    #         'title': 'Portable Power Bank', 
    #         'description': '10000mAh power bank with dual USB ports and LED indicator',
    #         'price': 45.99, 
    #         'stock': 25,
    #         'made_in': 'South Korea',
    #         'quantity': 1
    #     }
    # ]
    return render(request, 'shop/cart.html', { 'cart_items': lista_mea })

def payment(request):
    return render(request, 'shop/payment.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})