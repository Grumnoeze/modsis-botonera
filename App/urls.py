from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
]
