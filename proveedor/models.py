# coding=utf-8

from django.db import models

from producto.models import Producto
from general.models import DetallePedido, DevolucionPedido, Pedido


class Proveedor(models.Model):
    codigo = models.IntegerField(unique=True, verbose_name="Código")
    nit = models.CharField(max_length=10)
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=8, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")

    def __str__(self):
        return self.nombre


class PedidoProveedor(Pedido):
    proveedor = models.ForeignKey(Proveedor)

    def __str__(self):
        return self.fecha_pedido.strftime("Pedido hecho el %d de %m del %Y")


class DetallePedidoProveedor(DetallePedido):
    pedido = models.ForeignKey(PedidoProveedor)

    def __str__(self):
        return str(self.pedido)


class DevolucionPedidoProveedor(DevolucionPedido):
    detalle_pedido_proveedor = models.ForeignKey(DetallePedidoProveedor)

    def __str__(self):
        return self.detalle_pedido_proveedor.alias
