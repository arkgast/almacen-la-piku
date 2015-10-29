# coding=utf-8

from django.db import models

from simple_history.models import HistoricalRecords

# from producto.models import Producto
from general.models import (
    Pedido, DetallePedido,
    DevolucionPedido, DetalleDevolucionPedido
)


class Proveedor(models.Model):
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedor"

    codigo = models.IntegerField(unique=True, verbose_name="Código")
    nit = models.CharField(max_length=10)
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=8, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")

    def __str__(self):
        return self.nombre


# Pedido
class PedidoProveedor(Pedido):
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"

    proveedor = models.ForeignKey(Proveedor)
    total_pagado = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.fecha_pedido.strftime("Pedido hecho el %d de %m del %Y")

    def _precio_total(self):
        detalle_pedido = DetallePedidoProveedor.objects.filter(pedido=self)
        precio_total = 0
        for detalle in detalle_pedido:
            precio_total += detalle.cantidad_entregada * detalle.precio_compra
        return "%.2f" % (precio_total, )

    precio_total = property(_precio_total)

    def _saldo(self):
        detalle_pedido = DetallePedidoProveedor.objects.filter(pedido=self)
        precio_total = 0
        for detalle in detalle_pedido:
            precio_total += detalle.cantidad_entregada * detalle.precio_compra
        saldo = precio_total - self.total_pagado
        return "%.2f" % (saldo, )

    saldo = property(_saldo)

    def cancelado(self):
        detalle_pedido = DetallePedidoProveedor.objects.filter(pedido=self)
        precio_total = 0
        for detalle in detalle_pedido:
            precio_total += detalle.cantidad_entregada * detalle.precio_compra
        return self.total_pagado == precio_total

    cancelado.boolean = True


class DetallePedidoProveedor(DetallePedido):
    class Meta:
        verbose_name = "Detalle pedido"
        verbose_name_plural = "Detalle pedido"

    precio_compra = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pedido = models.ForeignKey(PedidoProveedor)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.producto)


# Devolución
class DevolucionPedidoProveedor(DevolucionPedido):
    proveedor = models.ForeignKey(Proveedor)

    class Meta:
        verbose_name = "Devolución pedido"
        verbose_name_plural = "Devolución pedido"

    def __str__(self):
        return str(self.proveedor)


class DetalleDevolucionPedidoProveedor(DetalleDevolucionPedido):
    devolucion_pedido_proveedor = models.ForeignKey(DevolucionPedidoProveedor)

    class Meta:
        verbose_name = "Detalle devolución"
        verbose_name_plural = "Detalle devolución"

    def __str__(self):
        return "DDPP" + str(self.devolucion_pedido_proveedor)
