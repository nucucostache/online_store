from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Account
from orders.models import Order, OrderLine
from shop.forms import ProductForm
from .models import Product, Category
from django.contrib import messages
from django.db import transaction

def cart(request):
    lista_mea = request.session.get('cart', [])
    # Calculate total cost with error handling
    total_cost = 0
    for item in lista_mea:
        try:
            # Get price from item or fetch from database
            if 'price' in item:
                price = float(item['price'])
            else:
                # Fetch price from database if not in cart
                try:
                    product = Product.objects.get(id=item['id'])
                    price = float(product.price)
                    item['price'] = price  # Add price to cart item for future use
                except Product.DoesNotExist:
                    price = 0
            quantity = int(item.get('quantity', 1))
            subtotal = price * quantity
            total_cost += subtotal
            item['subtotal'] = subtotal
            item['price'] = price  # Ensure price is always available
        except (ValueError, TypeError):
            item['subtotal'] = 0
            item['price'] = 0
    # Update session with corrected cart data
    request.session['cart'] = lista_mea
    request.session.modified = True
    # Get user's default address
    try:
        account = Account.objects.get(user=request.user)
        default_address = account.address if account.address else ''
    except Account.DoesNotExist:
        default_address = ''
    return render(request, 'shop/cart.html', {
        'cart_items': lista_mea,
        'total_cost': total_cost,
        'default_address': default_address
    })


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
        'quantity': 1,
        'price': float(product.price),  # Assuming you have a price field in your Product model)
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

def checkout(request):
    print(f"Checkout view called with method: {request.method}")
    if request.method == 'POST':
        cart_items = request.session.get('cart', [])
        delivery_address = request.POST.get('delivery_address', '').strip()
        print(f"Cart items: {cart_items}")
        print(f"Delivery address: {delivery_address}")
        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
        if not delivery_address:
            messages.error(request, 'Please provide a delivery address.')
            return redirect('cart')
        try:
            with transaction.atomic():
                # Get the user's account
                account = Account.objects.get(user=request.user)
                # Calculate total cost with error handling
                total_cost = 0
                for item in cart_items:
                    try:
                        # Get price from item or fetch from database
                        if 'price' in item:
                            price = float(item['price'])
                        else:
                            # Fetch price from database if not in cart
                            product = Product.objects.get(id=item['id'])
                            price = float(product.price)
                            item['price'] = price  # Add price to cart item
                        quantity = int(item.get('quantity', 1))
                        total_cost += price * quantity
                    except (ValueError, TypeError, Product.DoesNotExist) as e:
                        print(f"Error processing item {item}: {e}")
                        messages.error(request, f"Error processing cart item: {item.get('title', 'Unknown')}")
                        return redirect('cart')
                # Create the order
                order = Order.objects.create(
                    user=account,
                    total_cost=total_cost,
                    delivery_address=delivery_address,
                    status='pending'
                )
                print(f"Order created: {order.id}")
                # Create order lines for each cart item
                for item in cart_items:
                    try:
                        product = Product.objects.get(id=item['id'])
                        # Get price from item or product
                        price = float(item.get('price', product.price))
                        quantity = int(item.get('quantity', 1))
                        OrderLine.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=price
                        )
                        # Update product stock if needed
                        if hasattr(product, 'stock') and product.stock >= quantity:
                            product.stock -= quantity
                            product.save()
                    except Product.DoesNotExist:
                        print(f"Product {item['id']} not found")
                        continue
                    except (ValueError, TypeError) as e:
                        print(f"Error creating order line for {item}: {e}")
                        continue
                # Clear the cart
                request.session['cart'] = []
                request.session.modified = True
                messages.success(request, f'Order #{order.id} created successfully! Total: ${order.total_cost}')
                return redirect('products')
        except Account.DoesNotExist:
            messages.error(request, 'Account not found. Please create your profile.')
            return redirect('cart')
        except Exception as e:
            print(f"Error in checkout: {e}")
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('cart')
    else:
        # GET request - redirect to cart
        return redirect('cart')


def clear_cart(request):
    """Debug function to clear cart"""
    request.session['cart'] = []
    request.session.modified = True
    messages.success(request, 'Cart cleared!')
    return redirect('cart')


def remove_from_cart(request, product_id):
    """Remove a specific product from the cart"""
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, 'Product removed from cart.')
    return redirect('cart')



