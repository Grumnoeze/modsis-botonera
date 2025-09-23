from django.db import models
from django.contrib.auth.models import User

class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)

def __str__(self):
    return f"{self.usuario.username} - {self.rol}"

# Create your models here.
