import json
from urllib.parse import urlencode
from django.http import QueryDict
from django.http.response import JsonResponse
from .models import Product, Order, OrderItem
from .forms import ShippingAddressForm
from authentication.forms import CustomUserCreationForm


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
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
    
    
def guest_place_order(request, data):
    data['userInfo']['username'] = str(data['userInfo']['email']).split('@')[0]
    customer = CustomUserCreationForm(QueryDict(urlencode(data['userInfo']))).save()
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

    errors_data = {
        'errors': errors,
        'error_fields': error_fields,
        'success_fields': success_fields,
        'validation_error': validation_error,
    }
    
    return JsonResponse(errors_data, safe=False) if not data['reload'] else errors_data