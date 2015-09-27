# coding=utf-8

from django.db import models

from producto.models import Producto
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

    def __str__(self):
        return str(self.cliente)


class DetallePedidoCliente(DetallePedido):
    class Meta:
        verbose_name = "Detalle pedido"
        verbose_name_plural = "Detalle pedido"

    pedido = models.ForeignKey(PedidoCliente)

    def __str__(self):
        return str(self.pedido)


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
