import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .utils import login_form_validation


def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['loginInfo']['email']
        password = data['loginInfo']['password']
        
        if not data['reload']:
            return login_form_validation(request, data, email, password)
        else:
            login_form_validation(request, data, email, password)
            
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
    context = {}
    return render(request, 'authentication/login.html', context)


def register_user(request):
    context = {}
    return render(request, 'authentication/registration.html', context)