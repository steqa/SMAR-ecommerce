import json
from django.http.response import JsonResponse
from django.template.defaultfilters import date
from django.template.loader import render_to_string
from django.shortcuts import render
from store.models import Order
from .utils import is_valid_queryparam, is_valid_sortparam
from authentication.decorators import allowed_users


@allowed_users(allowed_roles=['seller'])
def dashboard(request):
    return render(request, 'sales_dashboard/dashboard.html')


@allowed_users(allowed_roles=['seller'])
def orders(request):
    orders = Order.objects.exclude(status=False)
    context = {
        'orders': orders,
    }
    return render(request, 'sales_dashboard/orders.html', context)

@allowed_users(allowed_roles=['seller'])
def order(request, pk):
    order = Order.objects.get(pk=pk)
    order_items = order.orderitem_set.all()
    shipping_address = order.shippingaddress_set.get()
    if request.method == 'POST':
        status = json.loads(request.body)['status']
        if status == '1' or status == '2' or status == '3':
            order.status = status
            order.save()
            date_updated = date(order.date_updated, 'm/d/Y G:i:s')
            
        return JsonResponse({'status': status, 'date_updated': date_updated}, safe=True)
    
    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    }
    return render(request, 'sales_dashboard/order-detail.html', context)


def orders_filter(request):
    orders = Order.objects.exclude(status=False)
    
    transaction_id = request.GET.get('transaction_id')
    email = request.GET.get('email')
    date_ordered_min = request.GET.get('date_ordered_min')
    date_ordered_max = request.GET.get('date_ordered_max')
    status = request.GET.get('status')
    
    if is_valid_queryparam(transaction_id):
        orders = orders.filter(transaction_id__icontains=transaction_id)
        
    if is_valid_queryparam(email):
        orders = orders.filter(customer__email__icontains=email)
        
    if is_valid_queryparam(date_ordered_min):
        orders = orders.filter(date_ordered__gte=(date_ordered_min + ' 00:00:00.000000+00:00'))
        
    if is_valid_queryparam(date_ordered_max):
        orders = orders.filter(date_ordered__lte=(date_ordered_max + ' 23:59:59.999999+00:00'))
        
    if is_valid_queryparam(status):
        orders = orders.filter(status=status)
        
    sort_transaction_id = request.GET.get('sort_transaction_id')
    sort_email = request.GET.get('sort_email')
    sort_date_ordered = request.GET.get('sort_date_ordered')
    sort_status = request.GET.get('sort_status')
    
    if is_valid_sortparam(sort_transaction_id):
        if sort_transaction_id == '1':
            orders = orders.order_by('-transaction_id')
        elif sort_transaction_id == '2':
            orders = orders.order_by('transaction_id')
    
    if is_valid_sortparam(sort_email):
        if sort_email == '1':
            orders = orders.order_by('-customer')
        elif sort_email == '2':
            orders = orders.order_by('customer')
    
    if is_valid_sortparam(sort_date_ordered):
        if sort_date_ordered == '1':
            orders = orders.order_by('-date_ordered')
        elif sort_date_ordered == '2':
            orders = orders.order_by('date_ordered')
    
    if is_valid_sortparam(sort_status):
        if sort_status == '1':
            orders = orders.order_by('-status')
        elif sort_date_ordered == '2':
            orders = orders.order_by('status')
    
    context = {
        'orders': orders,
    }
    
    return JsonResponse({
      'html': render_to_string('sales_dashboard/orders-list.html', context, request),
    })