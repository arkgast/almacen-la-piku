# coding=utf-8

from django.contrib import admin

from proveedor.models import Proveedor, PedidoProveedor, DetallePedidoProveedor, DevolucionPedidoProveedor


class DetallePedidoProveedorInline(admin.StackedInline):
    model = DetallePedidoProveedor
    extra = 1


class PedidoProveedorAdmin(admin.ModelAdmin):
    fields = ['fecha_pedido', 'estado']

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


admin.site.register(Proveedor)
admin.site.register(PedidoProveedor, PedidoProveedorAdmin)
admin.site.register(DevolucionPedidoProveedor)
