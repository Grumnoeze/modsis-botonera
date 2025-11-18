from .models import PerfilUsuario, FX, Programa, Rol


def es_jefe(user):
    try:
        return user.perfilusuario.rol == Rol.JEFE
    except PerfilUsuario.DoesNotExist:
        return False


def puede_editar_fx(user, fx: FX):
    if es_jefe(user):
        return True
    if fx.scope == FX.Scope.INSTITUCIONAL:
        return False  # solo jefe edita
    if fx.scope == FX.Scope.OPERADOR:
        return fx.propietario_id == user.id
    if fx.scope == FX.Scope.PROGRAMA:
        # Operador asignado al programa puede editar
        return fx.programa.operadores.filter(id=user.id).exists()
    return False


def puede_ver_fx(user, fx: FX):
    if es_jefe(user):
        return True
    if fx.scope == FX.Scope.INSTITUCIONAL:
        return True
    if fx.scope == FX.Scope.OPERADOR:
        return fx.propietario_id == user.id
    if fx.scope == FX.Scope.PROGRAMA:
        # Operador asignado o productor asignado puede ver
        return (
            fx.programa.operadores.filter(id=user.id).exists() or
            fx.programa.productores.filter(id=user.id).exists()
        )
    return False
