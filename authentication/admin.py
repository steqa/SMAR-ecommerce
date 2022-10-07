from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'fio', 'is_staff']
    
    add_fieldsets = (*UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields' : (
                    'email',
                    'fio',
                )
            }
        )
    )
    
    fieldsets = (*UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields' : (
                    'fio',
                )
            }
        )
    )
    