""" Configuraciones del admin de django """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Modelos
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','phone_number','is_admin')
    list_filter = ('is_admin','created','modified')
    
admin.site.register(User, CustomUserAdmin)
