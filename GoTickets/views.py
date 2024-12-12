from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event, Ticket
from rest_framework import viewsets
from .serializer import EventSerializer, TicketSerializer, UsuarioSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from .models import Ticket, Usuario
from django.contrib.auth import authenticate, login
from django.utils.datastructures import MultiValueDictKeyError





# Vistas básicas para los eventos, tickets y usuarios

def index(request):
    events = Event.objects.all()  # Obtiene todos los eventos de la base de datos
    return render(request, 'index.html', {'events': events})

def reserva(request):
    return render(request, 'reserva.html', {})

def misTickets(request):
    return render(request, 'misTickets.html', {})

def iniciarSesion(request):
    return render(request, 'iniciarSesion.html', {})

def registro(request):
    return render(request, 'registro.html', {})

def detalles(request):
    return render(request, 'detalles.html', {})

def event_detail(request, event_id):
    # Intentar obtener el evento con el ID proporcionado
    event = get_object_or_404(Event, pk=event_id)
    return render(request, "GoTickets/detail.html", {"event": event})

class EventViewSet(viewsets.ModelViewSet):
    queryset=Event.objects.all()
    serializer_class = EventSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class CompraView(APIView):
    @method_decorator(login_required)
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        # Inicializamos el formulario vacío
        form = Ticket(event=event)
        return render(request, 'compra.html', {'event': event, 'form': form})

    @method_decorator(login_required)
    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)

        if request.method == "POST":
            number_of_tickets = int(request.POST.get('number_of_tickets', 0))
            
            # Validamos la cantidad de tickets
            if number_of_tickets < 1:
                return render(request, 'compra.html', {'event': event, 'error': "Debe seleccionar al menos 1 ticket."})

            # Calculamos el precio total
            total_price = number_of_tickets * event.price

            # Crear el ticket (asociar el evento y el número de tickets)
            ticket = Ticket(event=event, user=request.user, number_of_tickets=number_of_tickets, precio=total_price)
            ticket.save()

            return render(request, 'compra_confirmacion.html', {'event': event, 'ticket': ticket})

class UsuarioViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def registrar(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True, 'message': 'Usuario registrado correctamente.', 'user_id': user.id})
        return Response({'success': False, 'errors': serializer.errors})

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre_completo = request.POST.get('nombre_completo')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        foto_perfil = request.FILES.get('foto_perfil')
        
        # Crear el usuario Django
        user = User.objects.create_user(username=username, password=password)
        
        # Guardar la información adicional del usuario
        usuario = Usuario(
            user=user,
            username=username,  # Asigna el nombre de usuario
            password=user.password,  # Guarda el hash de la contraseña
            nombre_completo=nombre_completo,
            direccion=direccion,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            foto_perfil=foto_perfil
        )
        usuario.save()
        
        # Autenticar y logear al usuario automáticamente después del registro
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la página principal después del registro
        
    return render(request, 'registro.html')



def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la página principal o a la página de eventos
        else:
            # No se pudo autenticar el usuario, redirige o muestra un mensaje de error
            return render(request, 'iniciarSesion.html', {'error': 'Credenciales inválidas'})
    return render(request, 'iniciarSesion.html')
