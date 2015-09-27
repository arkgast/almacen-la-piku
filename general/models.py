# coding=utf-8

from django.db import models

from producto.models import Producto


class Pedido(models.Model):
    fecha_pedido = models.DateField()
    estado = models.BooleanField(default=False)
    precio_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        abstract = True

    def getFechaPedido(self):
        return self.fecha_pedido.strftime("%d de %m del %Y")


class DetallePedido(models.Model):
    cantidad_solicitada = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cantidad_entregada = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)
    sub_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    producto = models.ForeignKey(Producto)

    class Meta:
        abstract = True


class DevolucionPedido(models.Model):
    fecha_devolucion = models.DateField(verbose_name="Fecha devolución")
    detalle = models.TextField()

    class Meta:
        abstract = True


class DetalleDevolucionPedido(models.Model):
    MOTIVOS = (
        ('PM', 'Producto en mal estado'),
        ('PV', 'Producto vencido')
    )
    producto = models.ForeignKey(Producto)
    cantidad_devuelta = models.DecimalField(max_digits=6, decimal_places=2)
    motivo = models.CharField(max_length=2, choices=MOTIVOS)

    class Meta:
        abstract = True
