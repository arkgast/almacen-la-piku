# coding=utf-8

import re
import datetime

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from cliente.models import (
    Cliente, PedidoCliente, DetallePedidoCliente,
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
    fields = ['producto', 'cantidad_solicitada', 'cantidad_entregada', 'precio_venta']
    min_num = 1
    model = DetallePedidoCliente
    show_change_link = False


class PedidoClienteAdmin(admin.ModelAdmin):
    fields = ['cliente', 'total_pagado']
    inlines = [DetallePedidoClienteInline]
    list_display = ('cliente', 'fecha_pedido', 'precio_total', 'total_pagado', 'saldo', 'cancelado', )
    list_editable = ('total_pagado', )
    list_filter = ('fecha_pedido', )
    search_fields = ['fecha_pedido', 'cliente__nombre']
    actions = ['generar_pdf']

    def generar_pdf(self, request, queryset):
        id = queryset[0].id
        pedido_id = PedidoCliente.encryptId(id)
        url = reverse('cliente:factura_pdf', kwargs={'pedido_id': pedido_id})
        return HttpResponseRedirect(url)

    generar_pdf.short_description = "Generar recibo"

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in formset.deleted_objects:
            if obj.cantidad_entregada is None:
                obj.cantidad_entregada = 0
            producto = obj.producto
            producto.stock += obj.cantidad_entregada
            producto.save()
            obj.delete()
        for instance in instances:
            if instance.cantidad_entregada is None:
                instance.cantidad_entregada = 0
            producto = instance.producto
            producto.stock -= instance.cantidad_entregada
            producto.save()
            instance.save()
        formset.save_m2m()


# Detalle Pedido Cliente - Is not in use
class DetallePedidoClienteAdmin(admin.ModelAdmin):
    fields = ['producto', 'cantidad_solicitada', 'cantidad_entregada', 'pedido']
    list_display = ['pedido', 'fechaPedido', 'producto', 'precio_venta', 'cantidad_solicitada', 'cantidad_entregada', 'subTotal']
    list_display_links = None
    list_filter = ['pedido__cliente__nombre']
    search_fields = ['pedido__cliente__nombre', 'producto__nombre']

    def subTotal(self, obj):
        return "%.2f Bs" % (obj.producto.precio_venta * obj.cantidad_entregada)

    subTotal.short_description = "Sub-Total"

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
        fields = ['cliente', 'detalle']

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
    # form = DevolucionPedidoClienteCreationForm

    fields = ['cliente', 'detalle']
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
            producto.stock += instance.cantidad_devuelta
            producto.save()
            instance.save()
        formset.save_m2m()


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(PedidoCliente, PedidoClienteAdmin)
admin.site.register(DevolucionPedidoCliente, DevolucionPedidoClienteAdmin)
# admin.site.register(DetallePedidoCliente, DetallePedidoClienteAdmin)
