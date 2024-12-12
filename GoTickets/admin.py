from django.contrib import admin

# Register your models here.
from .models import Event
admin.site.register(Event)

from .models import Ticket
admin.site.register(Ticket)

from .models import Usuario
admin.site.register(Usuario)