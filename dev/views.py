import datetime
import random
from urllib.parse import urlencode
from django.shortcuts import render
from django.http import QueryDict
from authentication.forms import CustomUserCreationForm
from .utils import generate_fio, generate_email, generate_password, generate_order, generate_order_item, generate_shipping_address


def generate_orders(request):
    if request.method == 'POST':
        if request.POST.get('quantity'):
            quantity = range(0, int(request.POST.get('quantity')))
            for q in quantity:
                year = random.randint(2004, 2022)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                hour = random.randint(1, 12)
                minute = random.randint(1, 59)
                second = random.randint(1, 59)
                microsecond = random.randint(1, 999999)
                date = datetime.datetime(year, month, day, hour, minute, second, microsecond)
                
                order = generate_order(date=date)
                quantity_order_items = random.randrange(1, 3)
                for q in range(0, quantity_order_items):
                    generate_order_item(order=order, date=date)
                
                generate_shipping_address(customer=order.customer, order=order, date=date)
    
    return render(request, 'generate-orders.html')


def generate_users(request):
    if request.method == 'POST':
        if request.POST.get('quantity'):
            quantity = range(0, int(request.POST.get('quantity')))
            for q in quantity:
                check = True
                while check:
                    fio = generate_fio()
                    email = generate_email()
                    password = generate_password()
                    user = {
                        'fio': fio,
                        'email': email,
                        'username': email,
                        'password1': password,
                        'password2': password,
                    }
                    user = CustomUserCreationForm(QueryDict(urlencode(user)))
                    if user.errors:
                        pass
                    else:
                        user.save()
                        check = False

    return render(request, 'generate-users.html')