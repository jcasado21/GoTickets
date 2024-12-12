from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from GoTickets import views
import os


router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')


urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('misTickets/', views.misTickets, name='misTickets'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('detalles/', views.detalles, name='detalles'),
    path('compra/<int:event_id>/', views.CompraView.as_view(), name='compra'),
    path('registro/', views.registro, name='registro'),

    path('comprar/<int:event_id>/', views.reserva, name='reserva'),  # URL para comprar un ticket
    path('', include(router.urls))
] 

# Incluye las rutas para archivos estáticos y de medios
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
