from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import FX, Programa, PerfilUsuario, Rol
from .permissions import puede_editar_fx, puede_ver_fx, es_jefe
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def crear_usuario_manual(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exists():
            return HttpResponse("El nombre de usuario ya existe, elige otro.")

        user = User.objects.create_user(username=username, password=password)
        from .models import PerfilUsuario
        PerfilUsuario.objects.create(usuario=user, rol=rol)
        return redirect('login')

    return render(request, 'pages/crear_usuario_manual.html')

@login_required
def registrar_usuario(request):
    if not request.user.PerfilUsuario.rol == 'JEFE':
        return HttpResponseForbidden("No tienes permisos para registrar usuarios.")

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'pages/registrar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Vista principal: muestra tabs de programas asignados, FX propios y FX institucionales
    programas_operador = Programa.objects.filter(operadores=request.user, activo=True)
    fx_propios = FX.objects.filter(scope=FX.Scope.OPERADOR, propietario=request.user, activo=True)
    fx_institucionales = FX.objects.filter(scope=FX.Scope.INSTITUCIONAL, activo=True)

    return render(request, 'pages/dashboard.html', {
        'programas': programas_operador,
        'fx_propios': fx_propios,
        'fx_institucionales': fx_institucionales,
        'es_jefe': es_jefe(request.user),
    })


@login_required
def programa_detalle(request, programa_id):
    programa = get_object_or_404(Programa, id=programa_id, activo=True)
    # Verificación de acceso: jefe, operador asignado o productor asignado
    if not (es_jefe(request.user) or
            programa.operadores.filter(id=request.user.id).exists() or
            programa.productores.filter(id=request.user.id).exists()):
        return HttpResponseForbidden("No tienes acceso a este programa.")

    fx_programa = FX.objects.filter(scope=FX.Scope.PROGRAMA, programa=programa, activo=True)
    return render(request, 'pages/programa.html', {'programa': programa, 'fx_programa': fx_programa})


@login_required
def fx_crear(request, scope, programa_id=None):
    # Form simple basado en POST; en producción usar ModelForm.
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        archivo = request.FILES.get('archivo')
        color = request.POST.get('color_boton', '')
        tecla = request.POST.get('tecla_rapida', '')
        volumen = float(request.POST.get('volumen_default', 1.0))

        fx = FX(nombre=nombre, archivo=archivo, color_boton=color, tecla_rapida=tecla, volumen_default=volumen)

        if scope == FX.Scope.INSTITUCIONAL:
            if not es_jefe(request.user):
                return HttpResponseForbidden("Solo el jefe puede crear FX institucionales.")
            fx.scope = FX.Scope.INSTITUCIONAL

        elif scope == FX.Scope.OPERADOR:
            fx.scope = FX.Scope.OPERADOR
            fx.propietario = request.user

        elif scope == FX.Scope.PROGRAMA:
            fx.scope = FX.Scope.PROGRAMA
            programa = get_object_or_404(Programa, id=programa_id)
            # Solo jefe u operador asignado puede crear
            if not (es_jefe(request.user) or programa.operadores.filter(id=request.user.id).exists()):
                return HttpResponseForbidden("No puedes crear FX para este programa.")
            fx.programa = programa

        fx.save()
        return redirect('dashboard')

    return render(request, 'pages/fx_form.html', {'scope': scope, 'programa_id': programa_id})


@login_required
def fx_editar(request, fx_id):
    fx = get_object_or_404(FX, id=fx_id)
    if not puede_editar_fx(request.user, fx):
        return HttpResponseForbidden("No tienes permisos para editar este FX.")

    if request.method == 'POST':
        fx.nombre = request.POST.get('nombre', fx.nombre)
        nuevo_archivo = request.FILES.get('archivo')
        if nuevo_archivo:
            fx.archivo = nuevo_archivo
        fx.color_boton = request.POST.get('color_boton', fx.color_boton)
        fx.tecla_rapida = request.POST.get('tecla_rapida', fx.tecla_rapida)
        fx.volumen_default = float(request.POST.get('volumen_default', fx.volumen_default))
        fx.save()
        return redirect('dashboard')

    return render(request, 'pages/fx_form.html', {'fx': fx})


@login_required
def fx_toggle_activo(request, fx_id):
    fx = get_object_or_404(FX, id=fx_id)
    if not puede_editar_fx(request.user, fx):
        return HttpResponseForbidden("No tienes permisos.")

    fx.activo = not fx.activo
    fx.save()
    return redirect('dashboard')


@login_required
def reproducir_fx(request, fx_id):
    # Backend solo responde ok; la reproducción real se hace en frontend con <audio> o Web Audio API.
    fx = get_object_or_404(FX, id=fx_id, activo=True)
    if not puede_ver_fx(request.user, fx):
        return HttpResponseForbidden("No tienes acceso a este FX.")
    return JsonResponse({
        'id': fx.id,
        'nombre': fx.nombre,
        'url': fx.archivo.url,
        'volumen_default': fx.volumen_default,
    })

