from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView, ListView
import pdb; 
from .models import Servicio, Cliente

# Create your views here.

##begin login & logout
import logging, logging.config
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect

def login(request):
    context = {}
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
            else:
                context['error'] = 'Non active user'
        else:
            context['error'] = 'Wrong username or password'
    except:
        context['error'] = ''
    
    populateContext(request, context)
    return HttpResponseRedirect("/")

def logout(request):
    context = {}
    try:
        auth_logout(request)
    except:
        context['error'] = 'Some error occured.'
    
    populateContext(request, context)
    return HttpResponseRedirect("/")

def populateContext(request, context):
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
        context['user'] = request.user

def isLoggegUser(request):    
    if request.user.is_authenticated() == True:
        return True

    return False
##end login & logout

class HomeIndexView(TemplateView):
    template_name = 'base.html'
    def get(self, request):
        context = {}
        populateContext(request, context)
        return render(request, self.template_name, context)

from django.core.urlresolvers import reverse
class ServiciosView(TemplateView):
    template_name = 'servicios.html'
    form = None

    def get(self, request):
        context = {}
        context['cliente']= False
        populateContext(request, context)
        return render(request, self.template_name, context)

    def post(self, request):
        stype = request.POST.get('searchType', 'No  hay datos')

        context = {}
        if (stype == 'NewService'):
            cliente = request.POST.get('noCliente', 'No  hay datos')
            context['tipobusqueda'] = 'crear servicio nuevo %s ' % cliente
            context['tipo']= True
            context['cliente']= cliente
            return redirect('ServicioCreateNewIndex',cliente)
        else:
            folio = request.POST.get('folioServicio', 'No  hay datos')
            context['tipobusqueda'] = 'revisar el status de un servicio %s' % folio
            context['tipo']= False
            try:
                x = Servicio.objects.get(folio=folio)
            except Servicio.DoesNotExist:
                x = None
            if ( x is None):
                context['errorFolioDetail'] = 'El FOLIO: [%s], No existe o no fue asignado a un servicio' % folio
                context['errorFolio'] = True
            else:
                return redirect('ServicioDetailIndex',x.pk)
        
        context['cliente']= True
        populateContext(request, context)
        return render(request, self.template_name, context)

class ServicioCreateNew(CreateView):
    template_name = 'servicio_form.html'
    model = Servicio
    fields = ('cliente','reporta','descripcion','status','coordinador','user')
    labels = ('Numero de Cliente','Persona quen reporta','Descricion del reporte',)

    def get_initial(self):
        code = self.kwargs['codigo']
        client = get_object_or_404(Cliente, codigo=code)
        # pdb.set_trace()
        # Get the initial dictionary from the superclass method
        initial = super(ServicioCreateNew, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['cliente'] = client
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServicioCreateNew, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        return context

# class ServicioUpdate(UpdateView):
#     model = Servicio
#     fields = ('status',)

class ServicioDetailView(DetailView):
    model = Servicio
    context_object_name = 'servicio'
    def get_template_names(self):
        return 'servicio_details.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServicioDetailView, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        return context

class CoordinacionTecnicaListView(ListView):
    model = Servicio
    context_object_name = 'servicios'
    def get_template_names(self):
        return 'coordinacion_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CoordinacionTecnicaListView, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        return context
