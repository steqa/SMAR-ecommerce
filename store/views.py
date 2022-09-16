from django.shortcuts import render
from .models import Product


def store(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def cart(request):
    context = {
        'count': range(5)
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {
        'count': range(5)
    }
    return render(request, 'store/checkout.html', context)