from django.db import models
from django.contrib.auth.models import User


class Rol(models.TextChoices):
    JEFE = "JEFE", "Jefe de Operadores"
    OPERADOR = "OPERADOR", "Operador Técnico"
    PRODUCTOR = "PRODUCTOR", "Productor"


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Rol.choices)
    # Opcional: área/turno, activo, etc.

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"


class Programa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    # Productores con acceso de lectura
    productores = models.ManyToManyField(User, related_name="programas_como_productor", blank=True)
    # Operadores asignados
    operadores = models.ManyToManyField(User, related_name="programas_como_operador", blank=True)
    # Activo/archivado
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CategoriaFX(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class FX(models.Model):
    # Tipo de pertenencia: institucional, del programa, o propio del operador
    class Scope(models.TextChoices):
        INSTITUCIONAL = "INSTITUCIONAL", "Institucional (público, editable solo por Jefe)"
        PROGRAMA = "PROGRAMA", "De programa"
        OPERADOR = "OPERADOR", "Propio del operador"

    nombre = models.CharField(max_length=120)
    archivo = models.FileField(upload_to="fx/")  # puedes usar storage S3/MinIO más adelante
    categoria = models.ForeignKey(CategoriaFX, on_delete=models.SET_NULL, null=True, blank=True)
    scope = models.CharField(max_length=20, choices=Scope.choices, default=Scope.PROGRAMA)

    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, null=True, blank=True, related_name="fx_programa")
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="fx_propios")

    volumen_default = models.FloatField(default=1.0) 
    color_boton = models.CharField(max_length=20, blank=True) # Color en formato hexadecimal o nombre CSS
    tecla_rapida = models.CharField(max_length=10, blank=True) # Representación de la tecla rápida

    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.scope == FX.Scope.PROGRAMA and not self.programa:
            raise ValidationError("FX de programa requiere asociar un Programa.")
        if self.scope == FX.Scope.OPERADOR and not self.propietario:
            raise ValidationError("FX propio requiere propietario (operador).")
        if self.scope == FX.Scope.INSTITUCIONAL and (self.programa or self.propietario):
            raise ValidationError("FX institucional no debe tener programa ni propietario.")

    def __str__(self):
        base = f"{self.nombre} [{self.scope}]"
        if self.programa:
            base += f" - {self.programa.nombre}"
        if self.propietario:
            base += f" - {self.propietario.username}"
        return base
