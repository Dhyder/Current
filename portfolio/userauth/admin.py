from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your custom user model

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (  
        ('USB Security', {'fields': ('usb_secret',)}),  
    )  

    add_fieldsets = UserAdmin.add_fieldsets + (  
        ('USB Security', {'fields': ('usb_secret',)}),  
    )  

    list_display = ('username', 'email', 'usb_secret')  # Add it to the list view

admin.site.register(CustomUser, CustomUserAdmin)
