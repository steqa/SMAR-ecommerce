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