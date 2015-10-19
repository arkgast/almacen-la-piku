# coding=utf-8

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from usuario.models import Usuario
from general import app_messages


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita su contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(app_messages.PASSWORD_MUST_MATCH)

        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UsuarioAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información de usuario', {'fields': ('date_of_birth', )}),
        ('Permisos', {'fields': ('is_admin', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


# admin.site.register(Usuario, UsuarioAdmin)
# admin.site.unregister(Group)

admin.site.site_header = "LA PIKU DELICATESSEN"
admin.site.disable_action('delete_selected')
