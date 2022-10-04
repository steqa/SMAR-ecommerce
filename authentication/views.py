from django.shortcuts import render


def login_user(request):
    context = {}
    return render(request, 'authentication/login.html', context)


def register_user(request):
    context = {}
    return render(request, 'authentication/registration.html', context)