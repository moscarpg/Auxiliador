from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Concurso, Materia, Aula, Tarefa
from datetime import date, datetime, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='/logar')
def home(request):
    concursos = Concurso.objects.filter(usuario=request.user)
    return render(request, "index.html", {"concursos": concursos})

@login_required(login_url='/logar')
def concursos(request):
    concursos = Concurso.objects.filter(usuario=request.user)
    return render(request, "concursos.html", {"concursos": concursos})

@login_required(login_url='/logar')
def cadastrarConcurso(request):
    usuario = request.user
    concurso = request.POST.get("concurso")
    Concurso.objects.create(nome=concurso, usuario=usuario)
    return redirect(concursos)

@login_required(login_url='/logar')
def removerConcurso(request, id):
    concurso = Concurso.objects.get(id=id)
    concurso.delete()
    return redirect(concursos)

@login_required(login_url='/logar')
def materias(request, id):
    concursos = Concurso.objects.filter(usuario=request.user)
    concurso = Concurso.objects.get(id=id)
    materias = Materia.objects.filter(concurso=concurso)
    aulas = Aula.objects.all()
    for materia in materias:
        materia.aulas = Aula.objects.filter(materia=materia).count()
    return render(request, "materias.html", {"materias": materias, "aulas": aulas, "concurso": concurso, "concursos": concursos})

@login_required(login_url='/logar')
def cadastrarMateria(request, id):
    novo_concurso = Concurso.objects.get(id=id)
    novo_nome = request.POST.get("nome")
    nova_especifica = request.POST.get("especifica") == 'on'
    novas_aulas = int(request.POST.get("aulas"))
    nova_materia = Materia.objects.create(nome=novo_nome, especifica=nova_especifica, aulas=novas_aulas, concurso=novo_concurso)
    for i in range(novas_aulas):
        Aula.objects.create(nome=f"Aula {i:02}", materia=nova_materia)
    return HttpResponseRedirect(f"/materias/{novo_concurso.id}")

@login_required(login_url='/logar')
def removerMateria(request, id):
    materia = Materia.objects.get(id=id)
    id_concurso = materia.concurso.id
    materia.delete()
    return HttpResponseRedirect(f"/materias/{id_concurso}")

@login_required(login_url='/logar')
def tarefas(request, id):
    concursos = Concurso.objects.filter(usuario=request.user)
    concurso = Concurso.objects.get(id=id)
    materias = Materia.objects.filter(concurso=concurso)
    aulas = [] 
    tarefas = []
    for materia in materias:
        aulas += Aula.objects.filter(materia=materia)
    for aula in aulas:
        tarefas += Tarefa.objects.filter(aula=aula)         
    for tarefa in tarefas:
        tarefa.data = tarefa.data.strftime(f"%Y-%m-%d")
        tarefa.data_revisao = tarefa.data_revisao.strftime(f"%Y-%m-%d")
    data_atual = date.today().strftime(f"%Y-%m-%d")
    return render(request, "tarefas.html", {"materias": materias, "aulas": aulas, "tarefas": tarefas, "data_atual": data_atual, "concurso": concurso, "concursos": concursos})

@login_required(login_url='/logar')
def cadastrarTarefa(request, id):
    concurso = Concurso.objects.get(id=id)
    nova_descricao = request.POST.get("descricao")
    novo_tempo = int(request.POST.get("tempo"))
    nova_data = datetime.strptime(request.POST.get("data"), f'%Y-%m-%d').date()
    nova_data_revisao = nova_data + timedelta(days=7)
    nova_aula = Aula.objects.get(id = request.POST.get("aula"))
    Tarefa.objects.create(descricao=nova_descricao, minutos=novo_tempo, data=nova_data, data_revisao=nova_data_revisao, aula=nova_aula)
    return HttpResponseRedirect(f"/tarefas/{concurso.id}")

@login_required(login_url='/logar')
def removerTarefa(request, id, id_concurso):
    tarefa = Tarefa.objects.get(id=id)
    tarefa.delete()
    return HttpResponseRedirect(f"/tarefas/{id_concurso}")

@login_required(login_url='/logar')
def editarTarefa(request, id, id_concurso):
    tarefa = Tarefa.objects.get(id=id)
    tarefa.descricao = request.POST.get("mudar_descricao")
    tarefa.minutos = request.POST.get("mudar_tempo")
    tarefa.data = datetime.strptime(request.POST.get("mudar_data"), f'%Y-%m-%d').date()
    tarefa.data_revisao = tarefa.data + timedelta(days=7)
    tarefa.aula = Aula.objects.get(id = request.POST.get("mudar_aula"))
    tarefa.save()
    return HttpResponseRedirect(f"/tarefas/{id_concurso}")

def cadastro(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect(logar)
    else:
        form_usuario = UserCreationForm()
    return render(request, 'cadastro.html', {'form_usuario': form_usuario})

def logar(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect(home)
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})

def deslogar(request):
    logout(request)
    return redirect(logar)