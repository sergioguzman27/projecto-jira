""" Views para usuarios """

# Django rest framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Permisos
from rest_framework.permissions import IsAuthenticated
from myapps.users.permissions import IsUserAdmin, DeletePermission, IsAccountOwner

# Modelos
from myapps.users.models import User
from myapps.works.models import Work

# Serializers
from myapps.users.serializers import (CreateUserSerializer, UserModelSerializer,
                                      UserLoginSerializer, UpdateUserSerializer,
                                      PermissionUserSerializer)

# Filtros
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    """ Viewset para los metodos de los usuarios """
    queryset = User.objects.filter(is_active=True)
    
    # Filtros
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('is_admin',)
    
    def get_permissions(self):
        permissions= []
        if self.action != 'login':
            permissions.append(IsAuthenticated)
        if self.action in ['create','permission','destroy']:
            permissions.append(IsUserAdmin)
        if self.action in ['update','partial_update']:
            permissions.append(IsAccountOwner)
        return [p() for p in permissions]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action in ['update','partial_update']:
            return UpdateUserSerializer
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'permission':
            return PermissionUserSerializer
        return UserModelSerializer
    
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data = request.data,
            context = self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        works = Work.objects.filter(responsible=user)
        if works.count() > 0:
            return Response({'menssage_error': 'El usuario tiene tareas asignadas'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """ Vista para el login, esta vista obtiene o crea el token """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """ Vista para logout del usuario, esta vista destruye el token """
        try:
            request.user.auth_token.delete()
        except (ObjectDoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response({"success": "Successfully logged out."},
                    status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'])
    def permission(self, request):
        """ Vista para cambiar de tipo a un usuario """
        queryset = User.objects.all()
        user = get_object_or_404(queryset,pk=request.data['id_user'])
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)
