from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('registration/', views.register_user, name='register-user'),
    path('logout/', views.logout_user, name='logout-user'),
]
