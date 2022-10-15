import json
from urllib.parse import urlencode
from django.http import QueryDict
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .utils import login_form_validation, register_user_form_validation
from .forms import CustomUserCreationForm
from .decorators import unathenticated_user


@unathenticated_user
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['loginInfo']['email']
        password = data['loginInfo']['password']
        validation_data = login_form_validation(request, email, password)
        
        if data['reload'] is False or validation_data['validation_error']:
            return JsonResponse(validation_data, safe=True)
        else:
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return JsonResponse({'reload': True}, safe=True)
        
    context = {}
    return render(request, 'authentication/login.html', context)


@unathenticated_user
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = CustomUserCreationForm(QueryDict(urlencode(data['registrationInfo'])))
        validation_data = register_user_form_validation(user)
        
        if data['reload'] is False or validation_data['validation_error']:
            return JsonResponse(validation_data, safe=True)
        else:
            user = user.save()
            login(request, user)
            return JsonResponse({'reload': True}, safe=True)
        
    context = {}
    return render(request, 'authentication/registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('login-user')