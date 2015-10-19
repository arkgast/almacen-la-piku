# coding=utf-8

from django.contrib import admin

from proveedor.models import (
    Proveedor, PedidoProveedor, DetallePedidoProveedor,
    DevolucionPedidoProveedor, DetalleDevolucionPedidoProveedor
)


# Proveedor
class ProveedorAdmin(admin.ModelAdmin):
    fields = ['nombre', 'nit', 'codigo', 'direccion', 'telefono']
    list_display = ['nombre', 'nit', 'codigo', 'telefono']
    search_fields = ['nombre', 'nit', 'codigo']


# Pedido Proveedor
class DetallePedidoProveedorInline(admin.TabularInline):
    model = DetallePedidoProveedor
    fields = ['producto', 'cantidad_solicitada', 'cantidad_entregada', 'precio_compra']

    extra = 1
    min_num = 1


class PedidoProveedorAdmin(admin.ModelAdmin):
    fields = ['proveedor']

    list_display = ('proveedor', 'fecha_pedido', 'precioTotal', 'estado', )
    list_filter = ('fecha_pedido', 'estado')
    search_fields = ['fecha_pedido', 'proveedor__nombre']

    inlines = [DetallePedidoProveedorInline]

    def precioTotal(self, obj):
        dps = DetallePedidoProveedor.objects.filter(pedido=obj)
        total = 0
        for dp in dps:
            total += dp.precio_compra * dp.cantidad_entregada
        return "%.2f Bs" % total

    precioTotal.short_description = "Precio Total"

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in formset.deleted_objects:
            if obj.cantidad_entregada is None:
                obj.cantidad_entregada = 0
            producto = obj.producto
            producto.stock -= obj.cantidad_entregada
            producto.save()
            obj.delete()
        for instance in instances:
            if instance.cantidad_entregada is None:
                instance.cantidad_entregada = 0
            producto = instance.producto
            producto.stock += instance.cantidad_entregada
            producto.save()
            instance.save()
        formset.save_m2m()


class DetalleDevolucionPedidoProveedorInline(admin.TabularInline):
    model = DetalleDevolucionPedidoProveedor
    extra = 1
    min_num = 1
    show_change_link = False


class DevolucionPedidoProveedorAdmin(admin.ModelAdmin):
    fields = ['proveedor', 'detalle']
    list_filter = ['fecha_devolucion']
    search_fields = ['proveedor__nombre']
    list_display = ['proveedor', 'fecha_devolucion', 'detalle']
    inlines = [DetalleDevolucionPedidoProveedorInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            if obj.cantidad_devuelta is None:
                obj.cantidad_devuelta = 0
            producto = obj.producto
            producto.stock += obj.cantidad_devuelta
            producto.save()
            obj.delete()
        for instance in instances:
            if instance.cantidad_devuelta is None:
                instance.cantidad_devuelta = 0
            producto = instance.producto
            producto.stock -= instance.cantidad_devuelta
            producto.save()
            instance.save()
        formset.save_m2m()


admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(PedidoProveedor, PedidoProveedorAdmin)
admin.site.register(DevolucionPedidoProveedor, DevolucionPedidoProveedorAdmin)
