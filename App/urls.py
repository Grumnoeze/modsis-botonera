from django.urls import path
from .views import (
    login_view, logout_view, dashboard,
    programa_detalle, fx_crear, fx_editar, fx_toggle_activo, reproducir_fx, registrar_usuario, crear_usuario_manual
)
from .models import FX

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registrar/', registrar_usuario, name='registrar'),
    path('crear-usuario/', crear_usuario_manual, name='crear_usuario_manual'),
    path('', dashboard, name='dashboard'),

    path('programa/<int:programa_id>/', programa_detalle, name='programa_detalle'),

    path('fx/crear/<str:scope>/', fx_crear, name='fx_crear'),
    path('fx/crear/<str:scope>/<int:programa_id>/', fx_crear, name='fx_crear_programa'),

    path('fx/<int:fx_id>/editar/', fx_editar, name='fx_editar'),
    path('fx/<int:fx_id>/toggle/', fx_toggle_activo, name='fx_toggle'),

    path('fx/<int:fx_id>/play/', reproducir_fx, name='fx_play'),

    

]
