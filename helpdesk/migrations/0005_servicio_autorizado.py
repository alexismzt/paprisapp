# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0004_auto_20150601_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='autorizado',
            field=models.NullBooleanField(),
        ),
    ]
