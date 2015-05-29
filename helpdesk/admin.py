from django.contrib import admin
from .models import Estados,Localidades,StatusCliente,StatusServicio,Prospecto,Articulo,Cliente,Orden,Servicio,Empleado, Sucursal
# Register your models here.

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('cliente','folio', 'user',)
    fields =('cliente','folio','reporta','descripcion','status', 'observaciones','coordinador', 'tecnico',)
    raw_id_fields = ('cliente',)
    def save_model(self, request, obj, form, change): 
        obj.user = request.user
        obj.save()
        
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'apellidop', 'apellidom','calle','numero',)
    search_fields = ('codigo', 'nombre', 'apellidop', 'apellidom', )

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('etype','name','user',)

class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre','direccion','numint','estado','municipio',)
    raw_id_fields = ('estado','municipio',)


admin.site.register(Estados)
admin.site.register(Localidades)
admin.site.register(StatusCliente)
admin.site.register(StatusServicio)
admin.site.register(Prospecto)
admin.site.register(Articulo)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Orden)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Servicio, ServicioAdmin)