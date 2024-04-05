from django.urls import path, re_path
from .views.usersView import * 

urlproyect = [
    # Ruta para la creación de registros a través de la API
    re_path(r'^person', usersView),
]
