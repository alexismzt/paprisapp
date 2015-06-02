# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0006_servicio_authobservacioenes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='statusCliente',
            field=models.CharField(default=b'2', max_length=1, choices=[(b'1', b'Al Corriente'), (b'2', b'Con Morosidad')]),
        ),
    ]
