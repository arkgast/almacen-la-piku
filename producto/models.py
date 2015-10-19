# coding=utf-8

from django.db import models


class Producto(models.Model):
    UNIDADES_DE_MEDIDA = (
        ('KG', 'Kilogramos'),
        ('LT', 'Litros'),
        ('UN', 'Unidades'),
    )
    codigo = models.PositiveIntegerField(unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=120)
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    stock = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cantidad disponible")
    unidad_de_medida = models.CharField(max_length=2, choices=UNIDADES_DE_MEDIDA)

    def __str__(self):
        return self.nombre
