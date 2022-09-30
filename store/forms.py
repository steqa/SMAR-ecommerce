from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import ShippingAddress


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            
            
class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'country', 'postcode']