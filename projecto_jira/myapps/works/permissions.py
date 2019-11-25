""" Permisos para las acciones con las tareas """

# Django rest framework
from rest_framework.permissions import BasePermission

# Modelos
from myapps.users.models import User
from myapps.works.models import Work

class IsResponsibleWork(BasePermission):
    """ Permiso que verifica si es el responsable de la tarea """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.responsible
    
class IsCreatorWork(BasePermission):
    """ Permiso que verifica si es el creador de la tarea """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin
