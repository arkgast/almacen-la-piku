# coding=utf-8

from django.db import models
from django.core.signing import Signer, BadSignature

from producto.models import Producto


class Pedido(models.Model):
    fecha_pedido = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def getFechaPedido(self):
        return self.fecha_pedido.strftime("%d de %m del %Y")

    @staticmethod
    def encryptId(pedido_id):
        signer = Signer()
        return signer.sign(pedido_id)

    @staticmethod
    def decryptId(encrypted_id):
        try:
            signer = Signer()
            return int(signer.unsign(encrypted_id))
        except BadSignature:
            return None


class DetallePedido(models.Model):
    cantidad_solicitada = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cantidad_entregada = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)
    cantidad_entregada_anterior = models.DecimalField(blank=True, default=0, max_digits=6, decimal_places=2)
    producto = models.ForeignKey(Producto)

    class Meta:
        abstract = True


class DevolucionPedido(models.Model):
    fecha_devolucion = models.DateField(auto_now=True)
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
