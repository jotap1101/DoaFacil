from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy


def index(request):
    """ Página inicial """
    context = {
        'user': request.user
    }
    return render(request, 'pages/index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if not request.POST.get('username') or not request.POST.get('password'):
            messages.error(request, 'Preencha todos os campos.')

            return redirect('login')
        
        try:
            user = Usuario.objects.get(username=request.POST.get('username'))
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

            return redirect('login')
        
        if not user.is_active:
            messages.error(request, 'Usuário inativo.')

            return redirect('login')
        
        if form.is_valid():
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

            if user is not None:
                login(request, user)
                messages.success(request, f'Bem vindo, {user.username}!')

                return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

            return redirect('login')
        
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'pages/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Sessão encerrada.')

    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)

        if not request.POST.get('username') or not request.POST.get('password1') or not request.POST.get('password2'):
            messages.error(request, 'Preencha todos os campos.')
            return redirect('register')
        
        if Usuario.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, 'Usuário já cadastrado.')
            return redirect('register')
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao cadastrar usuário.')
            return redirect('register')
    else:
        form = UsuarioCadastroForm()

    context = {
        'form': form
    }

    return render(request, 'pages/register.html',context)

@login_required(login_url= reverse_lazy('login'))
def doacoes_view(request):
    doacoes = Doacao.objects.all()
    add_doacao_form = DoacaoForm()
    edit_doacao_form = EditDoacaoForm(instance=Doacao())    
    item_form = ItemForm()
    context  = {
        'user': request.user,
        'doacoes': doacoes,
        'add_doacao_form': add_doacao_form,
        'edit_doacao_form': edit_doacao_form,
        'item_form': item_form
    }
    return render(request, 'pages/doacoes.html', context)

@login_required(login_url= reverse_lazy('login'))
def detalhes_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)
    doador = doacao.usuario  # Pegamos o usuário que fez a doação
    return render(request, 'pages/detalhes_doacao.html', {'doacao': doacao, 'doador': doador})

@login_required(login_url= reverse_lazy('login'))
def necessidades_view(request):
    necessidades = Necessidade.objects.all()
    necessidade_form = NecessidadeForm()
    item_form = ItemForm()
    context = {
        'necessidades': necessidades,
        'necessidade_form': necessidade_form,
        'item_form': item_form
    }
    return render(request, 'pages/necessidades.html', context)

@login_required(login_url= reverse_lazy('login'))
def cadastrar_doacao(request):
    if request.method == 'POST':
        doacao_form = DoacaoForm(request.POST)
        if doacao_form.is_valid():
            doacao = doacao_form.save(commit=False)
            doacao.usuario = request.user  # Associar a doação ao usuário logado
            doacao.save()
            messages.success(request, 'Doacao adicionado com sucesso!')
            return redirect('doacoes') 
        else:
            messages.error(request, 'Erro ao adicionar doacao.')
            return redirect('doacoes')  # Retornar para a página de cadastro de doações caso haja erro
    return redirect('doacoes')  # Redirecionar para a página de cadastro de doações caso o método da requisição não seja POST

@login_required(login_url= reverse_lazy('login'))
def cadastrar_necessidade(request):
    if request.method == 'POST':
        necessidade_form = NecessidadeForm(request.POST)
        if necessidade_form.is_valid():
            necessidade = necessidade_form.save(commit=False)
            necessidade.usuario = request.user
            necessidade.save()
            messages.success(request, 'Necessidade adicionada com sucesso!')
            return redirect('necessidades')
        else:
            messages.error(request, 'Erro ao adicionar necessidade.')
            return redirect('necessidades')
    return redirect('necessidades')

@login_required(login_url= reverse_lazy('login'))
def cadastrar_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.usuario = request.user
            item.save()
            messages.success(request, 'Item adicionado com sucesso!')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Erro ao adicionar item.')
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('index')

@login_required(login_url= reverse_lazy('login'))
def editar_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)

    if request.user != doacao.usuario:
        messages.error(request, 'Você não tem permissão para editar esta doação.')
        return redirect('doacoes')
    
    if request.method == 'POST':
        doacao_form = EditDoacaoForm(request.POST, instance=doacao)
        if doacao_form.is_valid():
            doacao_form.save()
            messages.success(request, 'Doação editada com sucesso!')
            return redirect('doacoes')
        else:
            messages.error(request, 'Erro ao editar doação.')
            return redirect('doacoes')
    return redirect('doacoes')
