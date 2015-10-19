# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleDevolucionPedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_devuelta', models.DecimalField(max_digits=6, decimal_places=2)),
                ('motivo', models.CharField(max_length=2, choices=[(b'PM', b'Producto en mal estado'), (b'PV', b'Producto vencido')])),
            ],
            options={
                'verbose_name': 'Detalle devoluci\xf3n',
                'verbose_name_plural': 'Detalle devoluci\xf3n',
            },
        ),
        migrations.CreateModel(
            name='DetallePedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_solicitada', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('cantidad_entregada', models.DecimalField(default=0, max_digits=6, decimal_places=2, blank=True)),
                ('precio_compra', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Detalle pedido',
                'verbose_name_plural': 'Detalle pedido',
            },
        ),
        migrations.CreateModel(
            name='DevolucionPedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_devolucion', models.DateField(auto_now=True)),
                ('detalle', models.TextField()),
            ],
            options={
                'verbose_name': 'Devoluci\xf3n pedido',
                'verbose_name_plural': 'Devoluci\xf3n pedido',
            },
        ),
        migrations.CreateModel(
            name='PedidoProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_pedido', models.DateField(auto_now=True)),
                ('estado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedido',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.IntegerField(unique=True, verbose_name=b'C\xc3\xb3digo')),
                ('nit', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=120)),
                ('telefono', models.CharField(max_length=8, verbose_name=b'Tel\xc3\xa9fono')),
                ('direccion', models.CharField(max_length=200, verbose_name=b'Direcci\xc3\xb3n')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedor',
            },
        ),
        migrations.AddField(
            model_name='pedidoproveedor',
            name='proveedor',
            field=models.ForeignKey(to='proveedor.Proveedor'),
        ),
        migrations.AddField(
            model_name='devolucionpedidoproveedor',
            name='proveedor',
            field=models.ForeignKey(to='proveedor.Proveedor'),
        ),
        migrations.AddField(
            model_name='detallepedidoproveedor',
            name='pedido',
            field=models.ForeignKey(to='proveedor.PedidoProveedor'),
        ),
        migrations.AddField(
            model_name='detallepedidoproveedor',
            name='producto',
            field=models.ForeignKey(to='producto.Producto'),
        ),
        migrations.AddField(
            model_name='detalledevolucionpedidoproveedor',
            name='devolucion_pedido_proveedor',
            field=models.ForeignKey(to='proveedor.DevolucionPedidoProveedor'),
        ),
        migrations.AddField(
            model_name='detalledevolucionpedidoproveedor',
            name='producto',
            field=models.ForeignKey(to='producto.Producto'),
        ),
    ]
