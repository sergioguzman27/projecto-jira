""" Modelo para tareas """

# Django
from django.db import models

# Modelo Base
from myapps.utils.models import ModelBase

class Work(ModelBase):
    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    # Existen tres tipos de estado, este campo guardara un numero de 1 a 3
    # 1: por hacer, 2:haciendo, 3:hecho
    state = models.CharField('Estado de la tarea',max_length=1, default='1')
    
    is_active = models.BooleanField(default=True)
    
    admin = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='admin',
        help_text='Usuario admin que creo la tarea'
    )
    
    responsible = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='responsible',
        help_text='Usuario responsable de la tarea'
    )
    
    class Meta:
        ordering = ['pk']
    
    def __str__(self):
        return '{} state: {}'.format(self.name, self.state)
    
