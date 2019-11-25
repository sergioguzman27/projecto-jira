""" Serializers utiles para los reportes """

# Django rest framework
from rest_framework import serializers

# Modelos
from myapps.works.models import Work
from myapps.users.models import User

# Serializers
from myapps.users.serializers import UserModelSerializer

class WorksReportSerializer(serializers.Serializer):
    """ Serializer  """
    
    to_do = serializers.IntegerField()
    doing = serializers.IntegerField()
    complete = serializers.IntegerField()
