# coding=utf-8
from functools import partial

from django import forms
from django.contrib import admin

from general import app_messages
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


class PedidoProveedorForm(forms.ModelForm):
    class Meta:
        model = PedidoProveedor
        fields = ['proveedor', 'total_pagado']

    def clean_total_pagado(self):
        total_pagado = self.cleaned_data.get("total_pagado")
        if total_pagado < 0:
            raise forms.ValidationError(app_messages.TOTAL_PAGADO_MUST_BE_POSITIVE)
        elif total_pagado > float(self.instance.precio_total):
            raise forms.ValidationError(app_messages.TOTAL_PAGADO_MUST_BE_LESS)
        return total_pagado


class PedidoProveedorAdmin(admin.ModelAdmin):
    form = PedidoProveedorForm
    fields = ['proveedor']
    list_display = ('proveedor', 'fecha_pedido', 'precio_total', 'total_pagado', 'saldo', 'cancelado', )
    list_editable = ('total_pagado', )
    list_filter = ('fecha_pedido', )
    search_fields = ['fecha_pedido', 'proveedor__nombre']

    inlines = [DetallePedidoProveedorInline]

    def get_changelist_formset(self, request, **kwargs):
        defaults = {
            "formfield_callback": partial(super(PedidoProveedorAdmin, self).formfield_for_dbfield, request=request),
            "form": PedidoProveedorForm,
        }
        defaults.update(kwargs)
        return forms.models.modelformset_factory(PedidoProveedor,
                                                 extra=0,
                                                 fields=self.list_editable, **defaults)

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
            if instance.cantidad_entregada_anterior is None:
                instance.cantidad_entregada_anterior = 0
            producto = instance.producto

            if instance.cantidad_entregada > instance.cantidad_entregada_anterior:
                cantidad_entregada = instance.cantidad_entregada - instance.cantidad_entregada_anterior
                producto.stock += instance.cantidad_entregada
            else:
                cantidad_entregada = instance.cantidad_entregada_anterior - instance.cantidad_entregada
                producto.stock -= instance.cantidad_entregada
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
