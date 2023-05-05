from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('concursos/', concursos, name="concursos"),
    path('cadastrarConcurso/', cadastrarConcurso, name="cadastrarConcurso"),
    path('removerConcurso/<int:id>', removerConcurso, name='removerConcurso'),

    path('materias/<int:id>', materias, name='materias'),
    path('cadastrarMateria/<int:id>', cadastrarMateria, name='cadastrarMateria'),
    path('removerMateria/<int:id>', removerMateria, name='removerMateria'),

    path('tarefas/<int:id>', tarefas, name='tarefas'),
    path('removerTarefa/<int:id>/<int:id_concurso>', removerTarefa, name='removerTarefa'),
    path('editarTarefa/<int:id>/<int:id_concurso>', editarTarefa, name='editarTarefa'),
    path('cadastrarTarefa/<int:id>', cadastrarTarefa, name='cadastrarTarefa'),

    path('cadastro/', cadastro, name="cadastro"),
    path('logar/', logar, name="logar"),
    path('deslogar', deslogar, name="deslogar"),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)