""" Views para tareas """

# Django rest framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Permisos
from rest_framework.permissions import IsAuthenticated
from myapps.users.permissions import IsUserAdmin
from myapps.works.permissions import IsCreatorWork, IsResponsibleWork

# Modelos
from myapps.users.models import User
from myapps.works.models import Work

# Serializers
from myapps.works.serializers import (WorkModelSerializer, CreateWorkSerializer,
                                      AssignmentUserSerializer, UpdateStateWorkSerializer)

# Filtros
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class WorkViewSet(viewsets.ModelViewSet):
    
    queryset = Work.objects.filter(is_active=True)
    
    # Filtros
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('state','responsible')
    
    def get_permissions(self):
        permissions= [IsAuthenticated]
        if self.action in ['create','created','unassigned','assigned']:
            permissions.append(IsUserAdmin)
        if self.action in ['update','partial_update','assignment','destroy']:
            permissions.append(IsCreatorWork)
        if self.action == 'state':
            permissions.append(IsResponsibleWork)
        return [p() for p in permissions]
    
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CreateWorkSerializer
        if self.action == 'assignment':
            return AssignmentUserSerializer
        if self.action == 'state':
            return UpdateStateWorkSerializer
        return WorkModelSerializer
    
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data = request.data,
            context = self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        work = serializer.save()
        data = WorkModelSerializer(work).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        work = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            work,
            data=request.data,
            context={'work': work},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        work = serializer.save()
        data = WorkModelSerializer(work).data
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def list(self, request):
        user = request.user
        if user.is_admin == True:
            queryset = Work.objects.filter(
                is_active=True
            )
        else:
            queryset = Work.objects.filter(
                responsible=user,
                is_active=True
            )
        query = self.filter_queryset(queryset)
        page = self.paginate_queryset(query)
        serializer_class = self.get_serializer_class()
        
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(query, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Usar getobjector404
        user = request.user
        if user.is_admin == True:
            queryset = Work.objects.filter(
                is_active=True
            )
        else:
            queryset = Work.objects.filter(
                responsible=user,
                is_active=True
            )
        work = get_object_or_404(queryset, pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(work)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        work = self.get_object()
        work.is_active = False
        work.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def created(self, request, *args, **kwargs):
        user = request.user
        queryset = Work.objects.filter(
            admin=user,
            is_active=True
        )
        query = self.filter_queryset(queryset)
        page = self.paginate_queryset(query)
        serializer_class = self.get_serializer_class()
        
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(query, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unassigned(self, request, *args, **kwargs):
        """ Vista para listar las tareas no asignadas a un usuairo que las creo """
        user = request.user
        queryset = Work.objects.filter(
            admin=user,
            responsible__isnull=True,
            is_active=True
        )
        query = self.filter_queryset(queryset)
        page = self.paginate_queryset(query)
        serializer_class = self.get_serializer_class()
        
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(query, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def assigned(self, request, *args, **kwargs):
        """ Vista para listar las tareas asignadas a un usuairo que las creo """
        user = request.user
        queryset = Work.objects.filter(
            admin=user,
            responsible__isnull=False,
            is_active=True
        )
        query = self.filter_queryset(queryset)
        page = self.paginate_queryset(query)
        serializer_class = self.get_serializer_class()
        
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(query, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assignment(self, request, *args, **kwargs):
        """ Vista para el asignar un usuario a una tarea """
        work = self.get_object()
        data = request.data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            work,
            data=request.data,
            context={'work': work},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        work = serializer.save()
        data = WorkModelSerializer(work).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['put'])
    def state(self, request, *args, **kwargs):
        """ Vista para cambiar el estado de una tarea """
        work = self.get_object()
        data = request.data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            work,
            data=request.data,
            context={'work': work},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        work = serializer.save()
        data = WorkModelSerializer(work).data
        return Response(data, status=status.HTTP_200_OK)
    
