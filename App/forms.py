from django import forms
from .models import usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = '__all__'
