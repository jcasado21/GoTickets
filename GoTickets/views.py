from datetime import datetime
from django.shortcuts import get_object_or_404, render
from .models import Event
from rest_framework import viewsets
from .serializer import EventSerializer, UsuarioSerializer
from .models import Event
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny



# Create your views here.
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

class UsuarioViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def registrar(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True, 'message': 'Usuario registrado correctamente.', 'user_id': user.id})
        return Response({'success': False, 'errors': serializer.errors})

