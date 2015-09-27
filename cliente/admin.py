# coding=utf-8

import re
import datetime

from django import forms
from django.contrib import admin

from cliente.models import (
    Cliente, PedidoCliente, 
    DetallePedidoCliente, DevolucionPedidoCliente,
    DevolucionPedidoCliente, DetalleDevolucionPedidoCliente,
)
from general import app_messages


# Cliente
class ClienteCreationForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'nit', 'telefono']

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if re.match("^([a-zA-ZñÑáéíóúÁÉÍÓÚ_-]\s?)+$", nombre) is None:
            raise forms.ValidationError(app_messages.NAME_MUST_BE_VALID)
        return nombre

    def clean_nit(self):
        nit = self.cleaned_data.get("nit")
        if nit.isdigit() is False:
            raise forms.ValidationError(app_messages.NIT_MUST_BE_VALID)
        return nit

    def save(self, commit=True):
        cliente = super(ClienteCreationForm, self).save(commit=False)
        if commit:
            cliente.save()
        return cliente


class ClienteAdmin(admin.ModelAdmin):
    form = ClienteCreationForm

    list_display = ['nombre', 'nit', 'telefono']
    search_fields = ['nombre', 'nit', 'telefono']


# Pedido Cliente

class DetallePedidoClienteInline(admin.TabularInline):
    extra = 1
    fields = ['producto', 'cantidad_solicitada', 'cantidad_entregada']
    min_num = 1
    model = DetallePedidoCliente
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


# Detalle Pedido Cliente
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


# Devolucion Pedido Cliente
class DetalleDevolucionPedidoClienteInline(admin.TabularInline):
    model = DetalleDevolucionPedidoCliente
    extra = 1
    min_num = 1
    show_change_link = False


class DevolucionPedidoClienteCreationForm(forms.ModelForm):
    class Meta:
        model = DevolucionPedidoCliente
        fields = ['cliente', 'fecha_devolucion', 'detalle']

    def clean_fecha_devolucion(self):
        fecha_devolucion = self.cleaned_data.get("fecha_devolucion")
        if fecha_devolucion < datetime.date.today():
            raise forms.ValidationError(app_messages.DATE_MUST_BE_GREATER)
        return fecha_devolucion

    def save(self, commit=True):
        devolucion_pedido_cliente = super(DevolucionPedidoClienteCreationForm, self).save(commit=False)
        if commit:
            devolucion_pedido_cliente.save()
        return devolucion_pedido_cliente


class DevolucionPedidoClienteAdmin(admin.ModelAdmin):
    #form = DevolucionPedidoClienteCreationForm

    fields = ['cliente', 'fecha_devolucion', 'detalle']
    list_filter = ['fecha_devolucion']
    search_fields = ['cliente__nombre']
    list_display = ['cliente', 'fecha_devolucion', 'detalle']
    inlines = [DetalleDevolucionPedidoClienteInline]

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


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(PedidoCliente, PedidoClienteAdmin)
admin.site.register(DevolucionPedidoCliente, DevolucionPedidoClienteAdmin)
# admin.site.register(DetallePedidoCliente, DetallePedidoClienteAdmin)
