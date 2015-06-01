# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0002_servicio_fechatermino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='dateAdded',
            field=models.DateField(auto_now_add=True),
        ),
    ]
