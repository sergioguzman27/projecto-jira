""" Modelo Base """

from django.db import models

class ModelBase(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creacion del objeto'
    )
    
    modified = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de modificacion del objeto'
    )
    
    class Meta:
        abstract = True
        get_latest_by='created'
        ordering = ['-created','-modified']
  
