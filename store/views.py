from django.shortcuts import render
from .models import Product, Order


def store(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
    else:
        order_items = []
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        
    context = {
        'order_items': order_items,
        'order': order,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
    else:
        order_items = []
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        
    context = {
        'order_items': order_items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)