from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('user/', include('authentication.urls')),
    path('dashboard/', include('sales_dashboard.urls')),
    path('dev/', include('dev.urls')),
]
