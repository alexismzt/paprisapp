from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

# Create your models here.
class Estados(models.Model):
    idEstado = models.CharField(max_length=10)
    idPais = models.CharField(max_length=10)
    nombreEstado = models.CharField(max_length=100)
    IdTipoRiesgo = models.CharField(max_length=1)
    idEstatus = models.CharField(max_length=1)
    def __unicode__(self):
        info = (self.nombreEstado[:20] + '..') if len(self.nombreEstado) > 20 else self.nombreEstado
        return info

class Localidades(models.Model):
    idEstado =models.CharField(max_length=10)
    idLocalidad=models.CharField(max_length=10)
    localidad=models.CharField(max_length=120)
    aliasCNBV=models.CharField(max_length=10)
    IdTipoRiesgo=models.CharField(max_length=1)
    idEstatus=models.CharField(max_length=1)
    def __unicode__(self):
        info = (self.localidad[:20] + '..') if len(self.localidad) > 20 else self.localidad
        return info

class Sucursal(models.Model):
    nombre = models.CharField(max_length=40)
    direccion = models.CharField(max_length=256)
    numint = models.CharField(max_length=10)
    numext = models.CharField(max_length=10)
    colonia = models.CharField(max_length=40)
    estado = models.ForeignKey(Estados, related_name = 'estado_sucursal')
    municipio = models.ForeignKey(Localidades, related_name = 'localidad_sucursal')
    def __unicode__(self):
        return self.nombre

class Empleado(models.Model):
    TIPO_EMPLEADO = (('0','SuperUser'),('1','Operador'),('2','Coordinador'),('3','Tecnico'),('4','Cobranza'))
    etype = models.CharField(max_length=1, choices=TIPO_EMPLEADO, default='1')
    name = models.CharField(max_length = 120)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    sucursal = models.ForeignKey(Sucursal, blank= True, null = True)
    def __unicode__(self):
        return ('[%s] %s') % (self.get_etype_display(), self.user)

class Prospecto(models.Model):
    title = models.CharField(max_length=25)
    def __unicode__(self):
        return self.title

class Articulo(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=256)
    precio = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateAdded = models.DateField(("Date"), auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ArticuloDetailIndex', kwargs={'pk': self.pk})

class Cliente(models.Model):
    TIPOPERSONA_CHOICE = (('1', 'Persona Moral'),('2', 'Persona Fisica'),('3', 'Persona Fisica con Ac. Empresarial'),)
    STATUSCLIENTE_CHOICE = (('1', 'Al Corriente'),('2', 'Con Morosidad'),)
    codigo = models.CharField(max_length=10)
    tipo = models.CharField(max_length=1, choices=TIPOPERSONA_CHOICE, default='2')
    nombre = models.CharField(max_length = 40)
    segundoNombre = models.CharField(max_length= 40, blank=True, null = True)
    apellidop = models.CharField(max_length = 40)
    apellidom = models.CharField(max_length = 40)
    rfc = models.CharField(max_length=13)
    calle = models.CharField(max_length=40)
    callead = models.CharField(max_length=40)
    numero = models.CharField(max_length=10)
    numext = models.CharField(max_length=10)
    codigopostal = models.CharField(max_length=5)
    colonia = models.CharField(max_length=40)
    estado = models.ForeignKey(Estados, related_name='+')
    localidad = models.ForeignKey(Localidades, related_name='+')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateAdded = models.DateField(("Date"), auto_now_add=True)
    statusCliente = models.CharField(max_length=1, choices=STATUSCLIENTE_CHOICE, default='1')
    
    def __unicode__(self):
        return '%s %s %s' % (self.nombre, self.apellidop, self.apellidom)

    def get_absolute_url(self):
        return reverse('ClienteDetailIndex', kwargs={'pk': self.pk})

    def get_domicilio(self):
        return '%s #%s CP: %s, Colonia: %s' % (self.calle, self.numero, self.codigopostal, self.colonia)

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, related_name = '+')
    total = models.FloatField()
    articulo = models.ManyToManyField(Articulo, related_name='+')
    descripcion = models.CharField(max_length=140)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateAdded = models.DateField(("Date"), auto_now_add=True)
    def __unicode__(self):
        return '%s %f' % (self.descripcion, self.total)

class Servicio(models.Model):
    STATUS_CHOICE = (('1', 'Pendiente'),('2', 'Cancelado'),('3', 'En progreso'),('4', 'Cerrado'))
    cliente = models.ForeignKey(Cliente, related_name='+')
    folio= models.IntegerField()
    reporta = models.CharField(max_length = 256)
    descripcion = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='1')
    observaciones = models.TextField(blank = True, null = True)
    coordinador = models.ForeignKey(Empleado, limit_choices_to={'etype': '2'}, blank= True, null = True)
    tecnico = models.ForeignKey(Empleado, limit_choices_to={'etype': '3'}, related_name = 'assigned_to', blank = True, null = True)
    ordenImpresa = models.FileField(upload_to='servicios/%Y/%m/%d', blank = True, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateAdded = models.DateTimeField(auto_now_add=True)
    fechaTermino = models.DateField(blank = True, null = True)
    autorizado = models.BooleanField(default=False)
    authObservacioenes = models.TextField(blank = True, null = True)
    fechaAsignacion = models.DateTimeField(blank=True, null=True)
    cerrado = models.BooleanField(default=False)

    def __unicode__(self):
        return '%i' % self.folio

    def save(self):
        if not self.pk:
            top = 0
            if (Servicio.objects.count() > 0):
                top = Servicio.objects.select_for_update(nowait=True).order_by('-folio')[0].folio
            self.created = True
            self.folio = top + 1

        super(Servicio, self).save()

    def get_absolute_url(self):
            return '/helpdesk/ServicioDetails/%d' % self.id

    def isAuthorized(self):
        if self.autorizado:
            return 'Si'
        else:
            return 'No'
