from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:pk>/', views.order_detail, name='order'),
    path('orders-filter/', views.orders_filter, name='orders-filter'),
    path('render-chart-data/', views.render_chart_data, name='render-chart-data'),
]
