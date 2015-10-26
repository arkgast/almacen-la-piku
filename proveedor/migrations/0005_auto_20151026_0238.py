# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0004_detallepedidoproveedor_cantidad_entregada_anterior'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedidoproveedor',
            name='precio_compra',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
        ),
    ]
