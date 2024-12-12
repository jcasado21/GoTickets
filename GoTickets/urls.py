from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from GoTickets import views
import os
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')


urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('misTickets/', views.misTickets, name='misTickets'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('detalles/', views.detalles, name='detalles'),
    path('compra/<int:event_id>/', views.CompraView.as_view(), name='compra'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    
    path('comprar/<int:event_id>/', views.reserva, name='reserva'),  # URL para comprar un ticket
    path('', include(router.urls))
] 

# Incluye las rutas para archivos estáticos y de medios
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
