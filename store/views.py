import json
import datetime
from django.http.response import JsonResponse
from django.template.defaultfilters import floatformat
from django.shortcuts import render
from .models import Product, Order, OrderItem, ShippingAddress


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_total_order_quantity
    else:
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        cart_items = order['get_total_order_quantity']
    
    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': cart_items,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_items = order.get_total_order_quantity
    else:
        order_items = []
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        cart_items = order['get_total_order_quantity']
        
    context = {
        'order_items': order_items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_items = order.get_total_order_quantity
    else:
        order_items = []
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        cart_items = order['get_total_order_quantity']
        
    context = {
        'order_items': order_items,
        'order': order,
        'cart_items': cart_items,
    }
    
    if request.user.is_authenticated:
        context['first_name'] = customer.first_name
        context['last_name'] = customer.last_name
        context['email'] = customer.email
        
    return render(request, 'store/checkout.html', context)


def update_order(request):
    data = json.loads(request.body)
    product_id = data['productID']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
        
    order_item.save()
    
    if order_item.quantity <= 0:
        order_item.delete()
        
    return JsonResponse({
        'cartItems': order.get_total_order_quantity,
        'productQuantity': order_item.quantity,
        'productTotalPrice': floatformat(order_item.get_total_items_price, '-2'),
        'totalOrderPrice': floatformat(order.get_total_order_price, '-2'),
        'totalOrderQuantity': order.get_total_order_quantity,
    }, safe=False)
    
    
def place_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_order_price = float(data['shippingInfo']['totalOrderPrice'].replace(',', '.'))
        order.transaction_id = transaction_id

        if total_order_price == float(order.get_total_order_price):
            order.complete = True
        order.save()
        
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shippingInfo']['address'],
            city=data['shippingInfo']['city'],
            country=data['shippingInfo']['country'],
            postcode=data['shippingInfo']['postcode'],
        )
    return JsonResponse('Payment complete!', safe=False)