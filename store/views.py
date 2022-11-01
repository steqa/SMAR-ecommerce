from django.shortcuts import render
from .models import Product
from .utils import cart_data, place_order, update_order


def store(request):
    products = Product.objects.all()
    data = cart_data(request)
    cart_total_quantity = data['cart_total_quantity']
    
    if request.method == 'POST':
        return update_order(request)

    context = {
        'products': products,
        'cart_total_quantity': cart_total_quantity,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cart_data(request)
    order = data['order']
    order_items = data['order_items']
    cart_total_quantity = data['cart_total_quantity']
    
    if request.method == 'POST':
        return update_order(request)
        
    context = {
        'order': order,
        'order_items': order_items,
        'cart_total_quantity': cart_total_quantity,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)
    order = data['order']
    order_items = data['order_items']
    cart_total_quantity = data['cart_total_quantity']
        
    if request.method == 'POST':
        return place_order(request)
    
    context = {
        'order': order,
        'order_items': order_items,
        'cart_total_quantity': cart_total_quantity,
    }
    
    if request.user.is_authenticated:
        context['fio'] = request.user.fio
        context['email'] = request.user.email
        
    return render(request, 'store/checkout.html', context)