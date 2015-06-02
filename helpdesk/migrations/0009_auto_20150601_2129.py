# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0008_auto_20150601_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='cerrado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='servicio',
            name='fechaAsignacion',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
