# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0003_auto_20150601_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='dateAdded',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
