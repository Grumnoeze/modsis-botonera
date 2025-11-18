from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario


class RegistroUsuarioForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = PerfilUsuario
        fields = ['rol']

    def save(self, commit=True):
        # Crear el usuario base de Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        # Crear el perfil asociado
        perfil = super().save(commit=False)
        perfil.usuario = user
        if commit:
            perfil.save()
        return perfil
