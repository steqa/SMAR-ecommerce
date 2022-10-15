from django.shortcuts import render
from store.models import ShippingAddress


def dashboard(request):
    return render(request, 'sales_dashboard/dashboard.html')


def orders(request):
    shippingaddresses = ShippingAddress.objects.all()
    context = {
        'shippingaddresses': shippingaddresses,
    }
    return render(request, 'sales_dashboard/orders.html', context)