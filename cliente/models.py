# coding=utf-8

from django.db import models

from producto.models import Producto
from general.models import (
    DevolucionPedido, DetalleDevolucionPedido, 
    Pedido, DetallePedido
)


class Cliente(models.Model):
    nit = models.CharField(max_length=10)
    nombre = models.CharField(max_length=120)
    telefono = models.PositiveIntegerField(verbose_name="Telefóno")

    def __str__(self):
        return self.nombre


class PedidoCliente(Pedido):
    cliente = models.ForeignKey(Cliente)

    def __str__(self):
        return str(self.cliente)


class DetallePedidoCliente(DetallePedido):
    pedido = models.ForeignKey(PedidoCliente)

    def __str__(self):
        return str(self.pedido)


class DevolucionPedidoCliente(DevolucionPedido):
    cliente = models.ForeignKey(Cliente)
    pedido = models.ForeignKey(PedidoCliente)

    def __str__(self):
        return str(self.cliente)


class DetalleDevolucionPedidoCliente(DetalleDevolucionPedido):
    devolucion_pedido = models.ForeignKey(DevolucionPedidoCliente)

    def __str__(self):
        return "DDPC " + str(self.devolucion_pedido)
