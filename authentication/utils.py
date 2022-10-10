from django.http.response import JsonResponse
from django.contrib.auth import authenticate
from .models import CustomUser


def login_form_validation(request, data, email, password):
    errors = {}
    error_fields = []
    success_fields = []

    if email != '':
        if not CustomUser.objects.filter(email=email).exists():
            error_fields.append('email')
            errors['email'] = 'Неверный адрес электронной почты.'
            validation_error = True
        else:
            success_fields.append('email')
            validation_error = False
            
    if password != '':
        if authenticate(request, email=email, password=password) is None:
            error_fields.append('password')
            errors['password'] = 'Неверный пароль.'
            validation_error = True
        else:
            success_fields.append('password')
            validation_error = False
    
    if email == '' or password == '':
        validation_error = True
        
    errors_data = {
        'errors': errors,
        'error_fields': error_fields,
        'success_fields': success_fields,
        'validation_error': validation_error,
        'reload': False,
    }
    
    return JsonResponse(errors_data, safe=False) if not data['reload'] else errors_data