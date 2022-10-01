from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-order/', views.update_order, name='update-order'),
    path('place-order/', views.place_order, name='place-order'),
    path('place-order-form-validation/', views.place_order_form_validation, name='place-order-form-validation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)