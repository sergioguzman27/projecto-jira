""" Views para los reportes """

# Django rest framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Permisos
from rest_framework.permissions import IsAuthenticated
from myapps.users.permissions import IsUserAdmin

# Modelos
from myapps.users.models import User
from myapps.works.models import Work

# Serializers
from myapps.reports.serializers import WorksReportSerializer

class ReportsViews(mixins.ListModelMixin,viewsets.GenericViewSet):
    
    def get_permissions(self):
        permissions= [IsAuthenticated]
        if self.action in ['advance','works']:
            permissions.append(IsUserAdmin)
        return [p() for p in permissions]
    
    def list(self, request):
        # Verificar si solo seran las de responsables
        user = request.user
        queryset = Work.objects.filter(
            responsible=user,
            is_active=True
        )
        to_do = queryset.filter(state='1').count()
        doing = queryset.filter(state='2').count()
        done = queryset.filter(state='3').count()
        
        data = {
            'to_do': to_do,
            'doing': doing,
            'done': done
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def works(self, request, *args, **kwargs):
        to_do = Work.objects.filter(state='1').count()
        doing = Work.objects.filter(state='2').count()
        done = Work.objects.filter(state='3').count()
        
        data = {
            'to_do': to_do,
            'doing': doing,
            'done': done
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def advance(self, request, *args, **kwargs):
        to_do = Work.objects.filter(state='1').count()
        doing = Work.objects.filter(state='2').count()
        done = Work.objects.filter(state='3').count()
        all_works = to_do + doing + done
        
        percent_to_do = round((to_do/all_works)*100,2)
        percent_doing = round((doing/all_works)*100,2)
        percent_done = round((done/all_works)*100,2)
        
        data = {
            'to_do': percent_to_do,
            'doing': percent_doing,
            'done': percent_done
        }
        return Response(data, status=status.HTTP_200_OK)
