import json
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from django.shortcuts import render
from store.models import Order


def dashboard(request):
    return render(request, 'sales_dashboard/dashboard.html')


def orders(request):
    orders = Order.objects.exclude(status=False)
    context = {
        'orders': orders,
    }
    return render(request, 'sales_dashboard/orders.html', context)


def orders_filter(request):
    orders = Order.objects.all()
    
    transaction_id = request.GET.get('transaction_id')
    email = request.GET.get('email')
    date_ordered_start = request.GET.get('date_ordered_start')
    date_ordered_end = request.GET.get('date_ordered_end')
    status = request.GET.get('status')
    
    if transaction_id != '' and transaction_id is not None:
        orders = orders.filter(transaction_id__icontains=transaction_id)
    
    return TemplateResponse(request, 'sales_dashboard/dashboard.html')