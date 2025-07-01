from django.shortcuts import get_object_or_404, redirect, render
from shop.forms import ProductForm
from .models import Product, Category

def cart(request):
    # lista_mea = Product.objects.all()
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
    lista_mea = request.session.get('cart', [])
    print(lista_mea)
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

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'product': product, 'form': form })

def products(request):
    productsFromDb = Product.objects.all()
    return render(request, 'shop/products.html', {'products': productsFromDb })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    product = get_object_or_404(Product, id=product_id)
    # cart.append(product)
    # request.session['cart'] = list(Product.objects.all().values('id', 'title', 'description', 'stock', 'made_in'))
    # request.session['cart'] = list(Product.objects.filter(id=product_id).values('id', 'title', 'description', 'stock', 'made_in'))

    # Check if the product is already in the cart
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            request.session['cart'] = cart
            return redirect('cart')

    cart.append({
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'stock': product.stock,
        'made_in': product.made_in,
        'thumbnail': product.thumbnail.url if product.thumbnail else None,
        'quantity': 1
    })
    request.session['cart'] = cart
    # cart.append(Product.objects.filter(id=product_id).values('id', 'title', 'description', 'stock', 'made_in'))
    return redirect('cart')

def delete_product(request, product_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    request.session['cart'] = cart
    return redirect('cart')


def product_table(request):
    productsFromDb = Product.objects.all()
    return render(request, 'shop/product_table.html', {'list_products': productsFromDb})


def all_categories(request):
    categoriesFromDb = Category.objects.all()
    return render(request, 'shop/categories.html', {'categories': categoriesFromDb})

def categories(request, category_id):
    category = get_object_or_404(Category, id=category_id)  
    lista_noastra = Product.objects.filter(category_id = category_id)  
    return render(request, 'shop/product_category.html', {'category_name' : category.name, 'list_products' : lista_noastra})

def successful_payment(request):
    return render(request, 'shop/successful_payment.html')    