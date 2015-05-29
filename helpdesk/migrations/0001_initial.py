# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=40)),
                ('descripcion', models.CharField(max_length=256)),
                ('precio', models.FloatField()),
                ('dateAdded', models.DateField(auto_now_add=True, verbose_name=b'Date')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=10)),
                ('tipo', models.CharField(default=b'2', max_length=1, choices=[(b'1', b'Persona Moral'), (b'2', b'Persona Fisica'), (b'3', b'Persona Fisica con Ac. Empresarial')])),
                ('nombre', models.CharField(max_length=40)),
                ('segundoNombre', models.CharField(max_length=40, null=True, blank=True)),
                ('apellidop', models.CharField(max_length=40)),
                ('apellidom', models.CharField(max_length=40)),
                ('rfc', models.CharField(max_length=13)),
                ('calle', models.CharField(max_length=40)),
                ('callead', models.CharField(max_length=40)),
                ('numero', models.CharField(max_length=10)),
                ('numext', models.CharField(max_length=10)),
                ('codigopostal', models.CharField(max_length=5)),
                ('colonia', models.CharField(max_length=40)),
                ('dateAdded', models.DateField(auto_now_add=True, verbose_name=b'Date')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etype', models.CharField(default=b'1', max_length=1, choices=[(b'0', b'SuperUser'), (b'1', b'Operador'), (b'2', b'Coordinador'), (b'3', b'Tecnico'), (b'4', b'Cobranza')])),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idEstado', models.CharField(max_length=10)),
                ('idPais', models.CharField(max_length=10)),
                ('nombreEstado', models.CharField(max_length=100)),
                ('IdTipoRiesgo', models.CharField(max_length=1)),
                ('idEstatus', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Localidades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idEstado', models.CharField(max_length=10)),
                ('idLocalidad', models.CharField(max_length=10)),
                ('localidad', models.CharField(max_length=120)),
                ('aliasCNBV', models.CharField(max_length=10)),
                ('IdTipoRiesgo', models.CharField(max_length=1)),
                ('idEstatus', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.FloatField()),
                ('descripcion', models.CharField(max_length=140)),
                ('dateAdded', models.DateField(auto_now_add=True, verbose_name=b'Date')),
                ('articulo', models.ManyToManyField(related_name='+', to='helpdesk.Articulo')),
                ('cliente', models.ForeignKey(related_name='+', to='helpdesk.Cliente')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prospecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folio', models.IntegerField()),
                ('reporta', models.CharField(max_length=256)),
                ('descripcion', models.TextField()),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('ordenImpresa', models.FileField(null=True, upload_to=b'servicios/%Y/%m/%d', blank=True)),
                ('dateAdded', models.DateField(auto_now_add=True, verbose_name=b'Date')),
                ('cliente', models.ForeignKey(related_name='+', to='helpdesk.Cliente')),
                ('coordinador', models.ForeignKey(blank=True, to='helpdesk.Empleado', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='StatusServicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('direccion', models.CharField(max_length=256)),
                ('numint', models.CharField(max_length=10)),
                ('numext', models.CharField(max_length=10)),
                ('colonia', models.CharField(max_length=40)),
                ('estado', models.ForeignKey(related_name='estado_sucursal', to='helpdesk.Estados')),
                ('municipio', models.ForeignKey(related_name='localidad_sucursal', to='helpdesk.Localidades')),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='status',
            field=models.ForeignKey(related_name='+', to='helpdesk.StatusServicio'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='tecnico',
            field=models.ForeignKey(related_name='assigned_to', blank=True, to='helpdesk.Empleado', null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='empleado',
            name='sucursal',
            field=models.ForeignKey(blank=True, to='helpdesk.Sucursal', null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.ForeignKey(related_name='+', to='helpdesk.Estados'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='localidad',
            field=models.ForeignKey(related_name='+', to='helpdesk.Localidades'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
