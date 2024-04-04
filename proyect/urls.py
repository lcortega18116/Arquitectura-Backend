from django.urls import path, re_path
from .views.views import * 

urlproyect = [
    # Ruta para la creación de registros a través de la API
    re_path(r'^vinculos', crdVinculos),
    re_path(r'^getimage', getimage),
    re_path(r'^background', deletebackground),
]
