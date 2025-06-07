from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Habito, Stats
from rest_framework.serializers import ModelSerializer


class HabitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habito
        fields = '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class StatSerializer(ModelSerializer):
    class Meta:
        model = Stats
        fields = ['id', 'usuario', 'streak', 'percentual_conclusao_mes']
        read_only_fields = ['usuario', 'percentual_conclusao_mes']