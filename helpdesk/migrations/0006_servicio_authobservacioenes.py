# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0005_servicio_autorizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='authObservacioenes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
