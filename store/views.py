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
        cart_total_quantity = order.get_total_order_quantity
    else:
        cart = json.loads(request.COOKIES['cart'])
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        for i in cart:
            order['get_total_order_quantity'] += cart[i]['quantity']
        cart_total_quantity = order['get_total_order_quantity']
    
    products = Product.objects.all()
    context = {
        'products': products,
        'cart_total_quantity': cart_total_quantity,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_total_quantity = order.get_total_order_quantity
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        
        order_items = []
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        for i in cart:
            product = Product.objects.get(id=i)
            product_total_price = product.price * cart[i]['quantity']
            order['get_total_order_price'] += product_total_price
            order['get_total_order_quantity'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity': cart[i]['quantity'],
                'get_total_items_price': product_total_price,
            }
            order_items.append(item)
        
        cart_total_quantity = order['get_total_order_quantity']
        
    context = {
        'order_items': order_items,
        'order': order,
        'cart_total_quantity': cart_total_quantity,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_total_quantity = order.get_total_order_quantity
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        
        order_items = []
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        for i in cart:
            product = Product.objects.get(id=i)
            product_total_price = product.price * cart[i]['quantity']
            order['get_total_order_price'] += product_total_price
            order['get_total_order_quantity'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity': cart[i]['quantity'],
                'get_total_items_price': product_total_price,
            }
            order_items.append(item)
        
        cart_total_quantity = order['get_total_order_quantity']
        
    context = {
        'order_items': order_items,
        'order': order,
        'cart_total_quantity': cart_total_quantity,
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
    
    if request.user.is_authenticated:
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
            
        productQuantity = order_item.quantity
        productPrice = floatformat(order_item.get_total_items_price, '-2g')
        cartTotalPrice = floatformat(order.get_total_order_price, '-2g')
        cartTotalQuantity = order.get_total_order_quantity
    else:
        cart = json.loads(request.COOKIES['cart'])
        order = {'get_total_order_price':0, 'get_total_order_quantity':0}
        for i in cart:
            product = Product.objects.get(id=i)
            order['get_total_order_price'] += product.price * cart[i]['quantity']
            order['get_total_order_quantity'] += cart[i]['quantity']
    
        try:
            productQuantity = cart[product_id]['quantity']
            productPrice = floatformat(product.price * productQuantity, '-2g')
        except:
            productPrice = 0
            productQuantity = 0
        cartTotalPrice = floatformat(order['get_total_order_price'], '-2g')
        cartTotalQuantity = order['get_total_order_quantity']
        
    return JsonResponse({
        'productQuantity': productQuantity,
        'productPrice': productPrice,
        'cartTotalPrice': cartTotalPrice,
        'cartTotalQuantity': cartTotalQuantity,
    }, safe=False)
    
    
def place_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_order_price = float(data['shippingInfo']['totalOrderPrice'].replace(',', '.'))

        if total_order_price == float(order.get_total_order_price) and total_order_price != 0:
            order.complete = True
            order.transaction_id = transaction_id
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shippingInfo']['address'],
                city=data['shippingInfo']['city'],
                country=data['shippingInfo']['country'],
                postcode=data['shippingInfo']['postcode'],
            )
            
        order.save()
        
    return JsonResponse('Payment complete!', safe=False)