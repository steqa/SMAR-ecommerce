from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from store.models import Order
from .utils import is_valid_queryparam


def dashboard(request):
    return render(request, 'sales_dashboard/dashboard.html')


def orders(request):
    orders = Order.objects.exclude(status=False)
    context = {
        'orders': orders,
    }
    return render(request, 'sales_dashboard/orders.html', context)


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
    
    context = {
        'orders': orders,
    }
    
    return JsonResponse({
      'html': render_to_string('sales_dashboard/orders-list.html', context, request),
    })