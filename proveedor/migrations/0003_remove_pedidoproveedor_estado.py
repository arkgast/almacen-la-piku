# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0002_pedidoproveedor_total_pagado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidoproveedor',
            name='estado',
        ),
    ]
