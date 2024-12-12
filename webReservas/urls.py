from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('GoTickets/', include('GoTickets.urls')),
    path('', include('GoTickets.urls')),  # Redirige la URL raíz a las URLs de webReservas
] 


# Incluye las rutas para archivos estáticos y de medios
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)