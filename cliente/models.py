# coding=utf-8

from django.db import models

from simple_history.models import HistoricalRecords

from general.models import (
    DevolucionPedido, DetalleDevolucionPedido,
    Pedido, DetallePedido
)


class Cliente(models.Model):
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Cliente"

    nit = models.CharField(max_length=10)
    nombre = models.CharField(max_length=120)
    telefono = models.PositiveIntegerField(verbose_name="Telefóno")

    def __str__(self):
        return self.nombre


class PedidoCliente(Pedido):
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"

    cliente = models.ForeignKey(Cliente)
    total_pagado = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.cliente)

    def _precio_total(self):
        detalle_pedido = DetallePedidoCliente.objects.filter(pedido=self)
        precio_total = 0
        for detalle in detalle_pedido:
            precio_total += detalle.cantidad_entregada * detalle.precio_venta
        return "%.2f" % (precio_total, )

    precio_total = property(_precio_total)

    def _saldo(self):
        detalle_pedido = DetallePedidoCliente.objects.filter(pedido=self)
        precio_total = 0
        for detalle in detalle_pedido:
            precio_total += detalle.cantidad_entregada * detalle.precio_venta

        saldo = precio_total - self.total_pagado
        return "%.2f" % (saldo, )

    saldo = property(_saldo)

    def cancelado(self):
        detalle_pedido = DetallePedidoCliente.objects.filter(pedido=self)
        precio_total = 0
        for detalle in detalle_pedido:
            precio_total += detalle.cantidad_entregada * detalle.precio_venta

        return self.total_pagado == precio_total

    cancelado.boolean = True


class DetallePedidoCliente(DetallePedido):
    class Meta:
        verbose_name = "Detalle pedido"
        verbose_name_plural = "Detalle pedido"

    precio_venta = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pedido = models.ForeignKey(PedidoCliente)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.producto)

    def _sub_total(self):
        return '%.2f Bs' % (self.cantidad_entregada * self.precio_venta, )

    sub_total = property(_sub_total)


class DevolucionPedidoCliente(DevolucionPedido):
    cliente = models.ForeignKey(Cliente)

    class Meta:
        verbose_name = "Devolución pedido"
        verbose_name_plural = "Devolución pedido"

    def __str__(self):
        return str(self.cliente)


class DetalleDevolucionPedidoCliente(DetalleDevolucionPedido):
    devolucion_pedido = models.ForeignKey(DevolucionPedidoCliente)

    class Meta:
        verbose_name = "Detalle devolución pedido"
        verbose_name_plural = "Detalle devolución pedido"

    def __str__(self):
        return "DDPC " + str(self.devolucion_pedido)
