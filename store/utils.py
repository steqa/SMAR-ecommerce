import datetime
import json
from urllib.parse import urlencode
from django.template.defaultfilters import floatformat
from django.http import QueryDict
from django.http.response import JsonResponse
from authentication.forms import CustomUserCreationForm
from .models import Product, Order, OrderItem, ShippingAddress
from .forms import ShippingAddressForm


def cookie_cart_data(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    order = {'get_total_order_price': 0, 'get_total_order_quantity': 0}
    order_items = []
    for i in cart:
        product = Product.objects.get(id=i)
        product_total_price = product.price * cart[i]['quantity']

        order['get_total_order_price'] += product_total_price
        order['get_total_order_quantity'] += cart[i]['quantity']

        order_item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image,
            },
            'quantity': cart[i]['quantity'],
            'get_total_items_price': product_total_price,
        }
        order_items.append(order_item)

    cart_total_quantity = order['get_total_order_quantity']

    return {
        'order_items': order_items,
        'order': order,
        'cart_total_quantity': cart_total_quantity,
        'cart': cart,
    }
    
    
def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, status=False)
        order_items = order.orderitem_set.all()
        cart_total_quantity = order.get_total_order_quantity
    else:
        cart = cookie_cart_data(request)
        order = cart['order']
        order_items = cart['order_items']
        cart_total_quantity = cart['cart_total_quantity']
        
    return {
        'order': order,
        'order_items': order_items,
        'cart_total_quantity': cart_total_quantity,
    }
    

def place_order(request):
    data = json.loads(request.body)
    validation_data = place_order_form_validation(request, data)
    if data['reload'] is False:
        return JsonResponse(validation_data, safe=True)
    
    total_order_price = float(data['totalOrderPrice'].replace(',', '.'))
    if validation_data['validation_error'] is False and (total_order_price > 0):
        transaction_id = datetime.datetime.now().timestamp()
    
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, status=False)
        else:
            customer, order = guest_place_order(request, data)
        
        if total_order_price == float(order.get_total_order_price):
            order.status = '1'
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
        return JsonResponse({'reload': True}, safe=True)
    else:
        return JsonResponse(validation_data, safe=True)

    
def guest_place_order(request, data):
    customer = CustomUserCreationForm(QueryDict(urlencode(data['userInfo']))).save()
    data_cart = cookie_cart_data(request)
    order_items = data_cart['order_items']
    
    order = Order.objects.create(
        customer = customer,
        status = False,
    )
    for item in order_items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity'],
        )
        
    return customer, order


def place_order_form_validation(request, data):
    errors = {}
    fields = ['fio', 'email', 'password1', 'password2', 'address', 'city', 'country', 'postcode']
    error_fields = []
    success_fields = []
    validation_error = False
    
    shipping_address_form = ShippingAddressForm(QueryDict(urlencode(data['shippingInfo'])))
    if shipping_address_form.errors:
        for field in shipping_address_form.errors:
            errors[field] = shipping_address_form.errors[field].as_text().replace('* ', '&bull;&nbsp;').replace('\n', '<br>')
            error_fields.append(field)
        validation_error = True

    if not request.user.is_authenticated:
        user_creation_form = CustomUserCreationForm(QueryDict(urlencode(data['userInfo'])))
        if user_creation_form.errors:
            for field in user_creation_form.errors:
                errors[field] = user_creation_form.errors[field].as_text().replace('* ', '&bull;&nbsp;').replace('\n', '<br>')
                error_fields.append(field)
            validation_error = True
    
    for f in fields:
        if f not in error_fields:
            success_fields.append(f)
        
    if request.user.is_authenticated:
        success_fields.remove('fio')
        success_fields.remove('email')
        success_fields.remove('password1')
        success_fields.remove('password2')

    errors_data = {
        'errors': errors,
        'error_fields': error_fields,
        'success_fields': success_fields,
        'validation_error': validation_error,
    }
    
    return errors_data


def update_order(request):
    data = json.loads(request.body)
    product_id = data['productID']
    action = data['action']
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, status=False)
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