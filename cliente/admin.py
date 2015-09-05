# coding=utf-8

from django.contrib import admin

from cliente.models import (
    Cliente, PedidoCliente, 
    DetallePedidoCliente, DevolucionPedidoCliente,
    DevolucionPedidoCliente, DetalleDevolucionPedidoCliente,
)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nit', 'telefono']


class DetallePedidoClienteInline(admin.TabularInline):
    model = DetallePedidoCliente
    extra = 1
    fields = [ 'producto', 'cantidad_solicitada', 'cantidad_entregada']
    min_num = 1
    show_change_link = False


class PedidoClienteAdmin(admin.ModelAdmin):
    fields = ['cliente', 'fecha_pedido', 'estado']
    inlines = [DetallePedidoClienteInline]
    list_display = ('cliente', 'fecha_pedido', 'precioTotal', 'estado', )
    list_filter = ('fecha_pedido', 'cliente__nombre')
    search_fields = ['fecha_pedido', 'cliente__nombre']


    def precioTotal(self, obj):
        dps = DetallePedidoCliente.objects.filter(pedido=obj)
        total = 0
        for dp in dps:
            total += dp.producto.precio_venta * dp.cantidad_entregada
        return "%.2f Bs" % total

    precioTotal.short_description = "Precio Total"

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            producto = obj.producto
            producto.stock -= obj.cantidad_entregada
            producto.save()
            obj.delete()
        for instance in instances:
            producto = instance.producto
            producto.stock += instance.cantidad_entregada
            producto.save()
            instance.save()
        formset.save_m2m()


class DetallePedidoClienteAdmin(admin.ModelAdmin):
    fields = ['producto', 'cantidad_solicitada', 'cantidad_entregada', 'pedido']
    list_display = ['pedido', 'fechaPedido', 'producto', 'precioVenta', 'cantidad_solicitada', 'cantidad_entregada', 'subTotal']
    list_display_links = None
    list_filter = ['pedido__cliente__nombre']
    search_fields = ['pedido__cliente__nombre', 'producto__nombre']

    def subTotal(self, obj):
        return "%.2f Bs" % (obj.producto.precio_venta * obj.cantidad_entregada)
    subTotal.short_description = "Sub-Total"

    def precioVenta(self, obj):
        return "%.2f Bs" % obj.producto.precio_venta
    precioVenta.short_description = "Precio Venta"

    def fechaPedido(self, obj):
        return obj.pedido.getFechaPedido()
    fechaPedido.short_description = "Fecha Pedido"


class DetalleDevolucionPedidoClienteInline(admin.TabularInline):
    model = DetalleDevolucionPedidoCliente
    extra = 1
    min_num = 1
    show_change_link = False


class DevolucionPedidoClienteAdmin(admin.ModelAdmin):
    fields = ['motivo', 'fecha_devolucion', 'detalle', 'pedido']
    inlines = [DetalleDevolucionPedidoClienteInline]



admin.site.register(Cliente, ClienteAdmin)
admin.site.register(PedidoCliente, PedidoClienteAdmin)
# admin.site.register(DetallePedidoCliente, DetallePedidoClienteAdmin)
admin.site.register(DevolucionPedidoCliente, DevolucionPedidoClienteAdmin)
