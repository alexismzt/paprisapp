#forms add here
from django import forms
from django.forms import ModelForm

from .models import Servicio, Cliente

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
		widgets = {
			'cliente' : forms.Select(attrs={'disabled':'disabled'}),
			'status' : forms.Select(attrs={'disabled':'disabled'}),
			'user' : forms.Select(attrs={'disabled':'disabled'}),
		}

class ServicioAsignacionForm(ModelForm):
	class Meta:
		model = Servicio
		fields = ('tecnico','fechaAsignacion',)
		labels = {
			'tecnico':'Asignar a Tecnico',
			'fechaAsignacion':'Fecha de Asignacion',
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

