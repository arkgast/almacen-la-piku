# coding=utf-8

from django.contrib import admin

from proveedor.models import (
    Proveedor, PedidoProveedor, 
    DetallePedidoProveedor, DevolucionPedidoProveedor,
    DevolucionPedidoProveedor, DetalleDevolucionPedidoProveedor
)


class DetallePedidoProveedorInline(admin.TabularInline):
    model = DetallePedidoProveedor
    fields = ['producto', 'cantidad_solicitada', 'cantidad_entregada']

    extra = 1
    min_num = 1


class PedidoProveedorAdmin(admin.ModelAdmin):
    fields = ['proveedor', 'fecha_pedido', 'estado']

    list_display = ('fecha_pedido', 'estado', )
    list_filter = ('fecha_pedido', )
    search_fields = ['fecha_pedido']

    inlines = [DetallePedidoProveedorInline]

    actions = ['pedido_entregado']

    def pedido_entregado(self, request, queryset):
        rows_updated = queryset.update(estado=True)
        if rows_updated == 1:
            message_bit = "1 pedido fue entregado"
        else:
            message_bit = "%s pedidos fueron entregados" % rows_updated
        self.message_user(request, message_bit)


    pedido_entregado.short_description = "Pedido Entregado"


class DetalleDevolucionPedidoProveedorInline(admin.TabularInline):
    model = DetalleDevolucionPedidoProveedor
    extra = 1
    min_num = 1
    show_change_link = False


class DevolucionPedidoProveedorAdmin(admin.ModelAdmin):
    fields = ['proveedor', 'fecha_devolucion', 'detalle']
    inlines = [DetalleDevolucionPedidoProveedorInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            producto = obj.producto
            producto.stock -= obj.cantidad_devuelta
            producto.save()
            obj.delete()
        for instance in instances:
            producto = instance.producto
            producto.stock -= instance.cantidad_devuelta
            producto.save()
            instance.save()
        formset.save_m2m()


admin.site.register(Proveedor)
admin.site.register(PedidoProveedor, PedidoProveedorAdmin)
admin.site.register(DevolucionPedidoProveedor, DevolucionPedidoProveedorAdmin)
