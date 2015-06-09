from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView, ListView
import pdb; 
from .models import Servicio, Cliente, Articulo, Orden, OrdenItem

from django.db.models import Q
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

from .forms import ServicioModelForm, ServicioAsignacionForm, ServicioCierreForm, ClienteCRMForm, ServicioEditForm, ArticulosInventoryForm, OrdenCRMForm, OrdenItemFormSet, OrdenItemCRMForm

class ServicioCreateNew(CreateView):
    template_name = 'servicio_form.html'
    model = Servicio
    form_class = ServicioModelForm
    clienteob = Cliente
    def get_initial(self):
        code = self.kwargs['codigo']
        client = get_object_or_404(Cliente, codigo=code)
        # pdb.set_trace()
        # Get the initial dictionary from the superclass method
        initial = super(ServicioCreateNew, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        self.clienteob = client
        initial['cliente'] = client
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServicioCreateNew, self).get_context_data(**kwargs)
        context['clientob'] = self.clienteob
        populateContext(self.request, context)
        return context

import datetime
class ServicioAsignacionUpdate(UpdateView):
    model = Servicio
    form_class = ServicioAsignacionForm
    context_object_name = 'servicioEdit'
    
    def get_template_names(self):
        return 'cobranza_update.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        # pdb.set_trace()
        initial = super(ServicioAsignacionUpdate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['fechaAsignacion'] = datetime.datetime.now()
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServicioAsignacionUpdate, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        context['cobranza'] = True
        return context

class ServicioEditUpdate(UpdateView):
    model = Servicio
    form_class = ServicioEditForm
    context_object_name = 'servicioEdit'
    
    def get_template_names(self):
        return 'cobranza_update.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        # pdb.set_trace()
        initial = super(ServicioEditUpdate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['fechaAsignacion'] = datetime.datetime.now()
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServicioEditUpdate, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        context['cobranza'] = True
        return context

class ServicioCierreUpdate(UpdateView):
    model = Servicio
    form_class = ServicioCierreForm
    context_object_name = 'servicioEdit'
    
    def get_template_names(self):
        return 'cobranza_update.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ServicioCierreUpdate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        serv = Servicio.objects.get(pk=self.kwargs['pk'])
        initial['fechaTermino'] = datetime.datetime.now().date()
        initial['cerrado'] = True
        initial['authObservacioenes'] = serv.authObservacioenes + '\r\n-----------------------\r\n'
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServicioCierreUpdate, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        context['cobranza'] = False
        return context


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
    queryset = Servicio.objects.order_by('-folio').filter(autorizado=True)
    model = Servicio
    context_object_name = 'servicios'
    paginate_by = 20  #and that's it !!

    def get_template_names(self):
        return 'coordinacion_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CoordinacionTecnicaListView, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        return context

class CobranzaListView(ListView):
    queryset = Servicio.objects.order_by('-folio').filter(autorizado=False)
    model = Servicio
    context_object_name = 'servicios'
    paginate_by = 20  #and that's it !!

    def get_template_names(self):
        return 'coordinacion_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CobranzaListView, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        context['cobranza'] = True
        return context

class CobranzaAuthorizeServiceUpdate(UpdateView):
    model = Servicio
    fields = ('autorizado','authObservacioenes',)
    context_object_name = 'servicioEdit'
    def get_template_names(self):
        return 'cobranza_update.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CobranzaAuthorizeServiceUpdate, self).get_context_data(**kwargs)
        populateContext(self.request, context)
        context['cobranza'] = True
        return context

from django.core.paginator import Paginator
class ClientesCRMListView(ListView):
    model = Cliente
    context_object_name = 'clientes'
    paginate_by = 20  #and that's it !!

    def get_template_names(self):
        return 'clienteCRM_list.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ClientesCRMListView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        return initial

    def get_queryset(self):
        #pdb.set_trace()
        if 'inputsearch' in self.request.GET:
            search = self.request.GET.get("inputsearch")
            if len(search) > 0:
                queryset = Cliente.objects.filter(Q(nombre__icontains=search) |Q(apellidop__icontains=search) |Q(apellidom__icontains=search) |Q(codigo__icontains=search))
            else:
                queryset = Cliente.objects.all()
        else:
                queryset = Cliente.objects.all()
        paginator = Paginator(queryset, 20) 
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClientesCRMListView, self).get_context_data(**kwargs)        
        
        q = self.request.GET.get("inputsearch")
        context['search'] = q
        
        populateContext(self.request, context)
        return context

class ClienteCRMDetailView(DetailView):
    model = Cliente
    context_object_name = 'cliente'
    def get_template_names(self):
        return 'cliente_index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClienteCRMDetailView, self).get_context_data(**kwargs)
        context['details'] = True
        populateContext(self.request, context)
        return context

class ClienteCRMUpdateView(UpdateView):
    model = Cliente
    context_object_name = 'cliente'
    form_class = ClienteCRMForm
    def get_template_names(self):
        return 'cliente_index.html'
    
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ClienteCRMUpdateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClienteCRMUpdateView, self).get_context_data(**kwargs)
        context['details'] = False
        populateContext(self.request, context)
        return context

class ClienteCRMCreateView(CreateView):
    model = Cliente
    context_object_name = 'cliente'
    form_class = ClienteCRMForm
    def get_template_names(self):
        return 'cliente_index.html'
    
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ClienteCRMCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClienteCRMCreateView, self).get_context_data(**kwargs)
        context['details'] = False
        populateContext(self.request, context)
        return context

class ArticulosInventoryCreateView(CreateView):
    model = Articulo
    context_object_name = 'articulo'
    form_class = ArticulosInventoryForm
    def get_template_names(self):
        return 'inventory_index.html'
    
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ArticulosInventoryCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticulosInventoryCreateView, self).get_context_data(**kwargs)
        context['modo'] = 'edit'
        populateContext(self.request, context)
        return context

class ArticulosInventoryListView(ListView):
    model = Articulo
    context_object_name = 'articulos'
    paginate_by = 20  #and that's it !!

    def get_template_names(self):
        return 'inventory_index.html'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ArticulosInventoryListView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticulosInventoryListView, self).get_context_data(**kwargs)
        context['modo'] = 'list'
        populateContext(self.request, context)
        return context

class ArticulosInventoryDetailView(DetailView):
    model = Articulo
    context_object_name = 'articulo'
    def get_template_names(self):
        return 'inventory_index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticulosInventoryDetailView, self).get_context_data(**kwargs)
        context['modo'] = 'details'
        populateContext(self.request, context)
        return context

class ArticulosInventoryUpdateView(UpdateView):
    model = Articulo
    context_object_name = 'articulo'
    form_class = ArticulosInventoryForm
    def get_template_names(self):
        return 'inventory_index.html'
    
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(ArticulosInventoryUpdateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticulosInventoryUpdateView, self).get_context_data(**kwargs)
        context['modo'] = 'edit'
        populateContext(self.request, context)
        return context

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        #pdb.set_trace()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        if hasattr(self, 'get_success_message'):
            self.get_success_message(form)
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class OrdenNewCreateView( CreateView):
    model = Orden
    form_class = OrdenCRMForm
    formset_class = OrdenItemFormSet

    def get_template_names(self):
        return 'orden_index.html'

    def get_initial(self):
        uid = self.kwargs['pk']
        client = get_object_or_404(Cliente, pk=uid)

        initial = super(OrdenNewCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        #self.clienteob = client
        initial['cliente'] = client
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(OrdenNewCreateView, self).get_context_data(**kwargs)
        context['modo'] = 'edit'
        populateContext(self.request, context)
        
        if self.request.POST:
            context['formset'] = OrdenItemFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = OrdenItemFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        #pdb.set_trace()
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())  # assuming your model has ``get_absolute_url`` defined.
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrdenDetailView(DetailView):
    model = Orden
    context_object_name = 'orden'
    def get_template_names(self):
        return 'orden_index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(OrdenDetailView, self).get_context_data(**kwargs)
        uid = self.kwargs['pk']
        context['items'] = OrdenItem.objects.filter(orden = uid)
        context['privatekey'] = uid
        context['modo'] = 'details'
        populateContext(self.request, context)
        return context
