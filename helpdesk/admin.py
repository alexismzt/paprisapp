from django.contrib import admin
from .models import Estados,Localidades,StatusCliente,StatusServicio,Prospecto,Articulo,Cliente,Orden,Servicio
# Register your models here.

admin.site.register(Estados)
admin.site.register(Localidades)
admin.site.register(StatusCliente)
admin.site.register(StatusServicio)
admin.site.register(Prospecto)
admin.site.register(Articulo)
admin.site.register(Cliente)
admin.site.register(Orden)
admin.site.register(Servicio)