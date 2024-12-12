from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


