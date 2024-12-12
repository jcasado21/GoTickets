
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event, Ticket
from rest_framework import viewsets
from .serializer import EventSerializer, TicketSerializer, UsuarioSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Ticket
from django.contrib.auth import authenticate, login

from .forms import RegistroUsuarioForm
from django.contrib import messages  # Para mostrar mensajes de error
from django.contrib.auth import logout
from django.shortcuts import redirect





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

def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar_sesion')  # Redirigir a la página de login después del registro
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro.html', {'form': form})



def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST['usuario']  # 'usuario' debe coincidir con el name del input
        password = request.POST['pass']  # 'pass' debe coincidir con el name del input
        
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Si las credenciales son válidas, iniciar sesión
            login(request, user)
            return redirect('index')  # Redirige a la URL del index
        else:
            # Si las credenciales no son válidas
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'iniciar_sesion.html')  # Renderiza el formulario si no es POST


def cerrar_sesion(request):
    logout(request)
    return redirect('index')  # Redirige al index o a cualquier otra página