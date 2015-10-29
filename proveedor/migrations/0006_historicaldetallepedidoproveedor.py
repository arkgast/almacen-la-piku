# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('producto', '__first__'),
        ('proveedor', '0005_auto_20151026_0238'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalDetallePedidoProveedor',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('cantidad_solicitada', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('cantidad_entregada', models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True)),
                ('cantidad_entregada_anterior', models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True)),
                ('precio_compra', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('pedido', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='proveedor.PedidoProveedor', null=True)),
                ('producto', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='producto.Producto', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Detalle pedido',
            },
        ),
    ]
