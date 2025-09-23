from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioForm
from .models import usuario

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('perfil')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def perfil_view(request):
    perfil = usuario.objects.get(usuario=request.user)
    return render(request, 'pages/perfil.html', {'perfil': perfil})

def home(request):
    return render(request, 'index.html')


# Create your views here.

