#forms add here
from django import forms
from django.forms import ModelForm

from .models import Servicio, Cliente, Articulo, Orden, OrdenItem
from django.forms.models import inlineformset_factory

class ServicioModelForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ('cliente','reporta','descripcion','status','coordinador','user',)
        labels = {
            'cliente' : 'Cliente',
            'reporta' : 'Persona que reporta',
            'descripcion' : 'Descripcion',
            'status': 'Status del Servicio',
            'coordinador' : 'Coordinador Asingado',
            'user':'Usuario que elaboro',
            }

class ServicioAsignacionForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ('tecnico','fechaAsignacion','status',)
        labels = {
            'tecnico':'Asignar a Tecnico',
            'fechaAsignacion':'Fecha de Asignacion',
            'status':'Status del servicio',
        }

class ServicioEditForm(ModelForm):
    class Meta:
        model = Servicio
        
        fields = ('folio','reporta','descripcion','status','coordinador','tecnico','ordenImpresa','fechaTermino','autorizado','authObservacioenes','fechaAsignacion','cerrado',)
        
        labels = {
            'folio' : 'Folio',
            'reporta' : 'Persona que reporta',
            'descripcion' : 'Descripcion',
            'status' : 'status',
            'coordinador' : 'Coordinador asignado',
            'tecnico' : 'Tecnico asignado',
            'ordenImpresa' : 'Archivo de Orden',
            'fechaTermino' : 'Fecha de termino',
            'autorizado' : 'Autorizado',
            'authObservacioenes' : 'Observacioenes',
            'fechaAsignacion' : 'Fecha de Asignacion',
            'cerrado' : 'cerrado',
        }

class ServicioCierreForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ('cerrado','fechaTermino','authObservacioenes','ordenImpresa',)
        labels = {
            'ordenImpresa':'Archivo de Orden',
            'fechaTermino':'Fecha de Cierre',
            'authObservacioenes' : 'Observaciones',
            'cerrado':'Cerrar',
        }

class ClienteCRMForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('codigo','tipo','nombre','segundoNombre','apellidop','apellidom','rfc','statusCliente','calle','callead','numero','numext','codigopostal','colonia','estado','localidad','user',)
        labels = {
            'codigo':'Codigo del cliente',
            'tipo':'Tipo de persona',
            'nombre':'Nombre',
            'segundoNombre':'Segundo Nombre',
            'apellidop':'Apellido Paterno',
            'apellidom':'Apellido Materno',
            'rfc':'RFC',
            'statusCliente':'Status',
            'calle':'Domicilio',
            'callead':'Adicional',
            'numero':'Numero exterior',
            'numext':'Numero interior',
            'codigopostal':'Codigo Postal',
            'colonia':'Colonia',
            'estado':'Estado',
            'localidad':'Localidad',
            'user':'user',
        }

class ArticulosInventoryForm(ModelForm):
    class Meta:
        model =Articulo
        fields=('code','title','descripcion','precio','user')

class OrdenCRMForm(ModelForm):
    class Meta:
        model = Orden
        fields =('cliente','descripcion', 'user',)
        labels = {
        'cliente' : 'Cliente',
        'descripcion' : 'Descripcion de la venta',
        'user' : 'Usuario:',
        }

class OrdenItemCRMForm(ModelForm):
    class Meta:
        model = OrdenItem
        fields = ('articulo','qty',)

OrdenItemFormSet = inlineformset_factory(Orden, OrdenItem, OrdenItemCRMForm, extra=0, min_num=1,)