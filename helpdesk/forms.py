#forms add here
from django import forms
from django.forms import ModelForm

from .models import Servicio

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