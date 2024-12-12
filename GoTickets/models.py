import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)  # Título del evento
    description = models.TextField()  # Descripción detallada del evento
    start_date = models.DateTimeField("start date")  # Fecha y hora de inicio
    end_date = models.DateTimeField("end date")  # Fecha y hora de finalización
    location = models.CharField(max_length=200)  # Ubicación del evento
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)  # Campo de imagen, opcional
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Precio del ticket
    
    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)  # Relación con el evento
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relación con el usuario que compra el ticket
    purchase_date = models.DateTimeField(auto_now_add=True)  # Fecha y hora de compra del ticket
    number_of_tickets = models.IntegerField()  # Número de tickets comprados
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Precio total de la compra

    def __str__(self):
        return f'Ticket {self.id} for {self.event.title}'


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User
    username = models.CharField(max_length=150, unique=True, default='usuario_anónimo')  # Nombre de usuario
    password = models.CharField(max_length=128, default='')  # Campo de contraseña (hasheada)
    nombre_completo = models.CharField(max_length=255)  # Nombre completo del usuario
    direccion = models.CharField(max_length=255, null=True, blank=True)  # Dirección del usuario, opcional
    telefono = models.CharField(max_length=20, null=True, blank=True)  # Número de teléfono del usuario, opcional
    fecha_nacimiento = models.DateField(null=True, blank=True)  # Fecha de nacimiento del usuario, opcional
    foto_perfil = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # Campo de imagen de perfil, opcional

    def __str__(self):
        return self.user.username  # Devuelve el nombre de usuario del usuario




