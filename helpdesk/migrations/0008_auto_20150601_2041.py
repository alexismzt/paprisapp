# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0007_cliente_statuscliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='statusCliente',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'1', b'Al Corriente'), (b'2', b'Con Morosidad')]),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='autorizado',
            field=models.BooleanField(default=False),
        ),
    ]
