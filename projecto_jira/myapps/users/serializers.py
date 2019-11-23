""" Serializers de usurio """

# Django rest framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Modelos
from myapps.users.models import User

# Django
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

class CreateUserSerializer(serializers.ModelSerializer):
    """ Serializer para crear usuarios """
    email = serializers.EmailField(
        validators = [
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators = [
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero no tiene el formato requerido'
    )
    
    phone_number = serializers.CharField(
        max_length=17,
        validators=[phone_regex]
    )
    
    password = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(min_length=2,max_length=30)
    last_name = serializers.CharField(min_length=2,max_length=30)
    is_admin = serializers.BooleanField(default=False)
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'is_admin'
        )
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators = [
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero no tiene el formato requerido'
    )
    
    phone_number = serializers.CharField(
        max_length=17,
        validators=[phone_regex]
    )
    
    password = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(min_length=2,max_length=30)
    last_name = serializers.CharField(min_length=2,max_length=30)
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'password'
        )

class UserModelSerializer(serializers.ModelSerializer):
    """ Serializer para listar usuarios """
    
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_admin',
            'created'
        )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales invalidas')
        self.context['user'] = user
        return data
    
    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class PermissionUserSerializer(serializers.Serializer):
    id_user = serializers.IntegerField()
    is_admin = serializers.BooleanField()
    
    def validate(self, data):
        try:
            user = User.objects.get(pk=data['id_user'])
        except User.DoesNotExist:
            raise serializers.ValidationError('El usuario no existe')
        self.context['user'] = user
        return data
    
    def update(self, instance, data):
        user = self.context['user']
        user.is_admin = data['is_admin']
        user.save()
        return user
            
