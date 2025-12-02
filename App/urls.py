from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    login_view, logout_view, dashboard,
    programa_detalle, fx_crear, fx_editar, 
    fx_toggle_activo, reproducir_fx, registrar_usuario,
    crear_usuario_manual, perfil_view, programa_crear
)
from .models import FX

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registrar/', registrar_usuario, name='registrar'),
    path('crear-usuario/', crear_usuario_manual, name='crear_usuario_manual'),
    path('perfil/', perfil_view, name='perfil'),
    path('', dashboard, name='dashboard'),

    path('programa/crear/', programa_crear, name='programa_crear'), 
    path('programa/<int:programa_id>/', programa_detalle, name='programa_detalle'),

    path('fx/crear/<str:scope>/', fx_crear, name='fx_crear'), 
    path('fx/crear/<str:scope>/<int:programa_id>/', fx_crear, name='fx_crear_programa'),
    path('fx/<int:fx_id>/editar/', fx_editar, name='fx_editar'),
    path('fx/<int:fx_id>/toggle/', fx_toggle_activo, name='fx_toggle'),
    path('fx/<int:fx_id>/play/', reproducir_fx, name='fx_play'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
