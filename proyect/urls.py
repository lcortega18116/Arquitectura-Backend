from django.urls import path, re_path
from .views.usersView import * 
from .views.classView import *
from .views.chatView import *
from .views.gradesView import *
from .views.presencesView import *

urlproyect = [
    # Ruta para la creación de registros a través de la API
    re_path(r'^person', usersView),
    re_path(r'^class', classView),
    re_path(r'^grade', gradesView),
    re_path(r'^presence', presencesView),
    re_path(r'^chat', chatView),
]
