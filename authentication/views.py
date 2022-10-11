import json
from urllib.parse import urlencode
from django.http import QueryDict
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .utils import login_form_validation, register_user_form_validation
from .forms import CustomUserCreationForm


def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['loginInfo']['email']
        password = data['loginInfo']['password']
        
        if data['reload'] is False:
            return login_form_validation(request, data, email, password)
        else:
            validation_data = login_form_validation(request, data, email, password)
            errors = validation_data['errors']
            error_fields = validation_data['error_fields']
            success_fields = validation_data['success_fields']
            validation_error = validation_data['validation_error']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                reload = True
            else:
                reload = False
            
            return JsonResponse({
                'errors': errors,
                'error_fields': error_fields,
                'success_fields': success_fields,
                'validation_error': validation_error,
                'reload': reload,
            }, safe=False)
        
    context = {}
    return render(request, 'authentication/login.html', context)


def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = CustomUserCreationForm(QueryDict(urlencode(data['registrationInfo'])))
        validation_data = register_user_form_validation(user)
        if data['reload'] is False:
            return JsonResponse(validation_data, safe=True)
        else:
            print(validation_data['errors'])
            if validation_data['validation_error'] is False:
                user = user.save()
                login(request, user)
                return JsonResponse({'reload': True}, safe=True)
        
    context = {}
    return render(request, 'authentication/registration.html', context)