from django.contrib import admin
from .models import PerfilUsuario, Programa, FX, CategoriaFX

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "rol")
    list_filter = ("rol",)

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    filter_horizontal = ("operadores", "productores")

@admin.register(FX)
class FXAdmin(admin.ModelAdmin):
    list_display = ("nombre", "scope", "programa", "propietario", "activo")
    list_filter = ("scope", "activo", "programa", "categoria")
    search_fields = ("nombre",)

admin.site.register(CategoriaFX)
