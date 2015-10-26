# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nit', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=120)),
                ('telefono', models.PositiveIntegerField(verbose_name=b'Telef\xc3\xb3no')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='DetalleDevolucionPedidoCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_devuelta', models.DecimalField(max_digits=6, decimal_places=2)),
                ('motivo', models.CharField(max_length=2, choices=[(b'PM', b'Producto en mal estado'), (b'PV', b'Producto vencido')])),
            ],
            options={
                'verbose_name': 'Detalle devoluci\xf3n pedido',
                'verbose_name_plural': 'Detalle devoluci\xf3n pedido',
            },
        ),
        migrations.CreateModel(
            name='DetallePedidoCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_solicitada', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('cantidad_entregada', models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True)),
                ('precio_venta', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Detalle pedido',
                'verbose_name_plural': 'Detalle pedido',
            },
        ),
        migrations.CreateModel(
            name='DevolucionPedidoCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_devolucion', models.DateField(auto_now=True)),
                ('detalle', models.TextField()),
                ('cliente', models.ForeignKey(to='cliente.Cliente')),
            ],
            options={
                'verbose_name': 'Devoluci\xf3n pedido',
                'verbose_name_plural': 'Devoluci\xf3n pedido',
            },
        ),
        migrations.CreateModel(
            name='PedidoCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_pedido', models.DateField(auto_now=True)),
                ('total_pagado', models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True)),
                ('cliente', models.ForeignKey(to='cliente.Cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedido',
            },
        ),
        migrations.AddField(
            model_name='detallepedidocliente',
            name='pedido',
            field=models.ForeignKey(to='cliente.PedidoCliente'),
        ),
        migrations.AddField(
            model_name='detallepedidocliente',
            name='producto',
            field=models.ForeignKey(to='producto.Producto'),
        ),
        migrations.AddField(
            model_name='detalledevolucionpedidocliente',
            name='devolucion_pedido',
            field=models.ForeignKey(to='cliente.DevolucionPedidoCliente'),
        ),
        migrations.AddField(
            model_name='detalledevolucionpedidocliente',
            name='producto',
            field=models.ForeignKey(to='producto.Producto'),
        ),
    ]
