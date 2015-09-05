# coding=utf-8

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from producto.models import Producto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_compra', 'precio_venta', 'fecha_vencimiento', 'stock')
    list_filter = ('fecha_vencimiento', )
    list_per_page = 20
    date_hierarchy = 'fecha_vencimiento'
    ordering = ('fecha_vencimiento', )
    search_fields = ['nombre', 'fecha_vencimiento']


admin.site.register(Producto, ProductoAdmin)
