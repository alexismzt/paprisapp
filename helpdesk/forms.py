#forms add here
from django import forms
from django.forms import ModelForm

from .models import Servicio

class ServicioModelForm(ModelForm):
	class Meta:
		model = Servicio
		fields = ('reporta','descripcion','status','observaciones','coordinador',)
		labels = (
			'Numero de Cliente','Persona quien reporta','Descricion del reporte',)