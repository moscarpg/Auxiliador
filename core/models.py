from django.db import models
from django.contrib.auth.models import User

class Concurso(models.Model):
    nome = models.CharField(max_length=40)
    usuario = models.ForeignKey(User , on_delete=models.CASCADE)

class Materia(models.Model):
    nome = models.CharField(max_length=40)
    especifica = models.BooleanField(default=False)
    aulas = models.IntegerField()
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE)

class Aula(models.Model):
    nome = models.CharField(max_length=10)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

class Tarefa(models.Model):
    descricao = models.CharField(max_length=255)
    minutos = models.IntegerField()
    data = models.DateField()
    data_revisao = models.DateField()
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)