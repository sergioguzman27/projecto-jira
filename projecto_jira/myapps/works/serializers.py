""" Serializers de usurio """

# Django rest framework
from rest_framework import serializers

# Modelos
from myapps.works.models import Work
from myapps.users.models import User

# Serializers
from myapps.users.serializers import UserModelSerializer

class WorkModelSerializer(serializers.ModelSerializer):
    """ Serializer para listar usuarios """
    admin = UserModelSerializer(read_only=True)
    responsible = UserModelSerializer(read_only=True)
    
    class Meta:
        model = Work
        fields = '__all__'

class CreateWorkSerializer(serializers.ModelSerializer):
    """ Serializer para crear tareas """

    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    admin = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id_responsible = serializers.IntegerField(required=False, min_value=1)
    
    class Meta:
        model = Work
        fields = ['name','description','admin','id_responsible']
        
    def validate(self, data):
        self.context['user'] = None
        if 'id_responsible' in data:
            print('Entro')
            id_user = data['id_responsible']
            try:
                user = User.objects.get(pk=id_user)
            except User.DoesNotExist:
                raise serializers.ValidationError('El usuario resposable no existe')
            self.context['user'] = user
        return data

    def create(self, data):
        user = self.context['user']
        work = Work.objects.create(
            name=data['name'],
            description=data['description'],
            admin=data['admin'],
            responsible=user)
        return work
    
    def update(self, instance, data):
        work = self.context['work']
        work.name = data['name']
        work.description = data['description']
        work.save()
        return work

class AssignmentUserSerializer(serializers.ModelSerializer):
    """ Serializer para asignar un usuario a una tarea """
    id_responsible = serializers.IntegerField(min_value=1)

    class Meta:
        model = Work
        fields = ['id_responsible']
    
    def validate_id_responsible(self, data):
        """ Se verifica que el usuario exista """
        try:
            responsible = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('El usuario resposable no existe')
        self.context['responsible'] = responsible
        return data
    
    def validate(self, data):
        """ Se valida que la tarea aun no este asignada a alguien """
        work = self.context['work']
        user = work.responsible
        if user is not None:
            raise serializers.ValidationError('La tarea ya se encuentra asignada')
        return data
    
    def update(self, instance, data):
        work = self.context['work']
        work.responsible = self.context['responsible']
        work.save()
        return work
    
class UpdateStateWorkSerializer(serializers.ModelSerializer):
    """ Serializer para modificar el estado de una tarea """
    
    state = serializers.CharField(min_length=1, max_length=1)
    
    class Meta:
        model = Work
        fields = ['state']
        
    def update(self, instance, data):
        work = self.context['work']
        work.state = data['state']
        work.save()
        return work
