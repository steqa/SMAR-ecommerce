from django.shortcuts import render
from store.models import Order
from .utils import render_chart_data, paginate_orders, filter_orders, change_order_status
from authentication.decorators import allowed_users


@allowed_users(allowed_roles=['seller'])
def dashboard(request):
    orders = Order.objects.exclude(status=False)

    if request.method == 'GET':
        if request.GET.get('get_chart_data'):
            return render_chart_data(request)

    context = {
        'orders': orders,
    }
    return render(request, 'sales_dashboard/dashboard.html', context)


@allowed_users(allowed_roles=['seller'])
def orders(request):
    orders = Order.objects.exclude(status=False)
    page_orders = paginate_orders(request, orders)
    
    if page_orders.paginator.num_pages == 1:
        displayed_orders = page_orders.paginator.object_list.count()
    else:
        displayed_orders = 20
        
    if request.method == 'GET':
        if request.GET.get('sort'):
            return filter_orders(request)
    
    context = {
        'orders': page_orders,
        'displayed_orders': displayed_orders,
        'total_orders': page_orders.paginator.object_list.count()
    }
    return render(request, 'sales_dashboard/orders.html', context)

@allowed_users(allowed_roles=['seller'])
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    order_items = order.orderitem_set.all()
    shipping_address = order.shippingaddress_set.get()
    if request.method == 'POST':
        return change_order_status(request, order)
    
    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    }
    return render(request, 'sales_dashboard/order-detail.html', context)