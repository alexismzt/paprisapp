# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0009_auto_20150601_2129'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StatusCliente',
        ),
        migrations.DeleteModel(
            name='StatusServicio',
        ),
        migrations.AlterField(
            model_name='servicio',
            name='status',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Pendiente'), (b'2', b'Cancelado'), (b'3', b'En progreso'), (b'4', b'Cerrado')]),
        ),
    ]
