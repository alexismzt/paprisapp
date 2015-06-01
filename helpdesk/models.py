from django.db import models
from django.conf import settings

# Create your models here.
class Estados(models.Model):
    idEstado = models.CharField(max_length=10)
    idPais = models.CharField(max_length=10)
    nombreEstado = models.CharField(max_length=100)
    IdTipoRiesgo = models.CharField(max_length=1)
    idEstatus = models.CharField(max_length=1)
    def __unicode__(self):
        return self.nombreEstado

class Localidades(models.Model):
    idEstado =models.CharField(max_length=10)
    idLocalidad=models.CharField(max_length=10)
    localidad=models.CharField(max_length=120)
    aliasCNBV=models.CharField(max_length=10)
    IdTipoRiesgo=models.CharField(max_length=1)
    idEstatus=models.CharField(max_length=1)
    def __unicode__(self):
        return '%s' % self.localidad

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

class StatusCliente(models.Model):
    title = models.CharField(max_length= 25)
    def __unicode__(self):
        return self.title

class StatusServicio(models.Model):
    title = models.CharField(max_length=25)
    def __unicode__(self):
        return self.title

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

class Cliente(models.Model):
    TIPOPERSONA_CHOICE = (('1', 'Persona Moral'),('2', 'Persona Fisica'),('3', 'Persona Fisica con Ac. Empresarial'),)
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
    
    def __unicode__(self):
        return '%s %s %s' % (self.nombre, self.apellidop, self.apellidom)

    def get_absolute_url(self):
        return reverse('cliente-detail', kwargs={'pk': self.pk})

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, related_name = '+')
    total = models.FloatField()
    articulo = models.ManyToManyField(Articulo, related_name='+')
    descripcion = models.CharField(max_length=140)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateAdded = models.DateField(("Date"), auto_now_add=True)
    def __unicode__(self):
        return '%s %f' % (sefl.descripcion, self.total)

class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='+')
    folio= models.IntegerField()
    reporta = models.CharField(max_length = 256)
    descripcion = models.TextField()
    status = models.ForeignKey(StatusServicio, related_name='+')
    observaciones = models.TextField(blank = True, null = True)
    coordinador = models.ForeignKey(Empleado, limit_choices_to={'etype': '2'}, blank= True, null = True)
    tecnico = models.ForeignKey(Empleado, limit_choices_to={'etype': '3'}, related_name = 'assigned_to', blank = True, null = True)
    ordenImpresa = models.FileField(upload_to='servicios/%Y/%m/%d', blank = True, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateAdded = models.DateField(("Date"), auto_now_add=True)
    fechaTermino = models.DateField(blank = True, null = True)

    def __unicode__(self):
        return '%i' % self.folio

    def save(self): 
        top = 0
        if (Servicio.objects.count() > 0):
            top = Servicio.objects.select_for_update(nowait=True).order_by('-folio')[0].folio
        self.folio = top + 1
        super(Servicio, self).save()

    def get_absolute_url(self):
            return '/helpdesk/ServicioDetails/%d' % self.id 
