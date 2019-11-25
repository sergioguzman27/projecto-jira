""" Permisos para las acciones con usuarios """

# Django rest framework
from rest_framework.permissions import BasePermission

# Modelos
from myapps.users.models import User

class IsUserAdmin(BasePermission):
    """ Permiso que verifica si el usuario es admin """
    def has_permission(self, request, view):
        user = request.user
        if user.is_admin == True:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin == True:
            return True
        return False

class DeletePermission(BasePermission):
    """ Permiso para eliminar """
    def has_object_permission(self, request, view, obj):
        return False
    
class IsAccountOwner(BasePermission):
    """ Permiso para editar si es el usuario el que lo manda """
    def has_object_permission(self, request, view, obj):
        return request.user == obj
