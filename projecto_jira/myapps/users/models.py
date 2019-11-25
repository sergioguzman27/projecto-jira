""" Modelos de Usuarios """

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Modelo Base
from myapps.utils.models import ModelBase

class User(ModelBase, AbstractUser):
    
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'El email debe ser unico'
        }
    )
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero no tiene el formato requerido'
    )
    
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        validators=[phone_regex]
    )
    
    is_admin = models.BooleanField('tipo de usuario',default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        ordering = ['pk']
    
    def __str__(self):
        return self.username
    
    def get_short_name(self):
        return self.username
