# coding=utf-8

import datetime

from django import forms
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from producto.models import Producto
from general import app_messages


class ProductoCreationForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'precio_compra', 'precio_venta', 'fecha_vencimiento', 'stock', 'unidad_de_medida']

    def clean_precio_compra(self):
        precio = self.cleaned_data.get("precio_compra")
        if precio <= 0:
            raise forms.ValidationError(app_messages.PRICE_MUST_BE_POSITIVE)
        return precio

    def clean_precio_venta(self):
        precio = self.cleaned_data.get("precio_venta")
        if precio <= 0:
            raise ValueError(app_messages.PRICE_MUST_BE_POSITIVE)
        return precio

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get("fecha_vencimiento")
        if fecha_vencimiento <= datetime.date.today():
            raise forms.ValidationError(app_messages.DATE_MUST_BE_GREATER)
        return fecha_vencimiento

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 0:
            raise forms.ValidationError(app_messages.STOCK_MUST_BE_POSITIVE)
        return stock

    def save(self, commit=True):
        producto = super(ProductoCreationForm, self).save(commit=False)
        if commit:
            producto.save()
        return producto


class ProductoAdmin(admin.ModelAdmin):
    form = ProductoCreationForm

    date_hierarchy = 'fecha_vencimiento'
    list_display = ('nombre', 'codigo', 'precio_compra', 'precio_venta', 'fecha_vencimiento', 'stock')
    list_filter = ('fecha_vencimiento', )
    list_per_page = 20
    ordering = ('fecha_vencimiento', )
    search_fields = ['nombre', 'codigo', 'fecha_vencimiento']


admin.site.register(Producto, ProductoAdmin)
