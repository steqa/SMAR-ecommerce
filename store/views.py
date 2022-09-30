import json
import datetime
from urllib.parse import urlencode
from django.http import QueryDict
from django.http.response import JsonResponse
from django.template.defaultfilters import floatformat
from django.shortcuts import render
from .models import Product, Order, OrderItem, ShippingAddress
from .utils import cookie_cart_data, cart_data
from .forms import CustomUserCreationForm, ShippingAddressForm


def store(request):
    products = Product.objects.all()
    data = cart_data(request)
    cart_total_quantity = data['cart_total_quantity']

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
        
    context = {
        'order': order,
        'order_items': order_items,
        'cart_total_quantity': cart_total_quantity,
    }
    
    if request.user.is_authenticated:
        context['first_name'] = request.user.first_name
        context['last_name'] = request.user.last_name
        context['email'] = request.user.email
        
    return render(request, 'store/checkout.html', context)


def update_order(request):
    data = json.loads(request.body)
    product_id = data['productID']
    action = data['action']
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
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
        data_cart = cookie_cart_data(request)
        order = data_cart['order']
        cart = data_cart['cart']
        
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
    total_order_price = float(data['totalOrderPrice'].replace(',', '.'))
    
    errors = {}
    fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'address', 'city', 'country', 'postcode']
    error_fields = []
    success_fields = []
    validation_error = False
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        user_creation_form = CustomUserCreationForm(QueryDict(urlencode(data['userInfo'])))
        shipping_address_form = ShippingAddressForm(QueryDict(urlencode(data['shippingInfo'])))
        if user_creation_form.is_valid() and shipping_address_form.is_valid() and total_order_price != 0:
            customer = user_creation_form.save()
            data_cart = cookie_cart_data(request)
            order_items = data_cart['order_items']
            
            order = Order.objects.create(
                customer = customer,
                complete = False,
            )
            for item in order_items:
                product = Product.objects.get(id=item['product']['id'])
                order_item = OrderItem.objects.create(
                    product = product,
                    order = order,
                    quantity = item['quantity'],
                )
        else:
            validation_error = True
                    
    if validation_error:
        for field in user_creation_form.errors:
            errors[field] = user_creation_form.errors[field].as_text().replace('* ', '&bull;&nbsp;').replace('\n', '<br>')
            error_fields.append(field)
            
        for field in shipping_address_form.errors:
            errors[field] = shipping_address_form.errors[field].as_text().replace('* ', '&bull;&nbsp;').replace('\n', '<br>')
            error_fields.append(field)
            
        for f in fields:
            if f not in error_fields:
                success_fields.append(f)
    else:
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
        else:
            validation_error = True
        
        order.save()
            
    return JsonResponse({
        'errors': errors,
        'error_fields': error_fields,
        'success_fields': success_fields,
        'validation_error': validation_error,
    }, safe=False)