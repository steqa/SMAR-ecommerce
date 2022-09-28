import json
from .models import Product, Order


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
        customer = request.user.customer
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