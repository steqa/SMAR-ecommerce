from django.urls import path
from . import views

urlpatterns = [
    path('generate-orders', views.generate_orders, name='generate-orders'),
    path('generate-users', views.generate_users, name='generate-users'),
]
