from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doacao, Necessidade, Instituicao
from .forms import DoacaoForm, NecessidadeForm


def index(request):
    """ Página inicial """
    doacoes = Doacao.objects.filter(status='Disponível')[:5]
    instituicoes = Instituicao.objects.all()[:5]
    necessidades = Necessidade.objects.filter(aprovado_por_admin=True)[:5]
    return render(request, 'index.html', {'doacoes': doacoes, 'instituicoes': instituicoes, 'necessidades': necessidades})


@login_required
def cadastrar_doacao(request):
    """ Cadastro de uma nova doação """
    if request.method == 'POST':
        form = DoacaoForm(request.POST)
        if form.is_valid():
            doacao = form.save(commit=False)
            doacao.doador = request.user.doador
            doacao.save()
            return redirect('index')
    else:
        form = DoacaoForm()
    return render(request, 'cadastrar_doacao.html', {'form': form})


@login_required
def cadastrar_necessidade(request):
    """ Cadastro de uma nova necessidade por uma instituição """
    if request.method == 'POST':
        form = NecessidadeForm(request.POST)
        if form.is_valid():
            necessidade = form.save(commit=False)
            necessidade.instituicao = request.user.instituicao
            necessidade.save()
            return redirect('index')
    else:
        form = NecessidadeForm()
    return render(request, 'cadastrar_necessidade.html', {'form': form})


def listar_doacoes(request):
    """ Lista de todas as doações disponíveis """
    doacoes = Doacao.objects.filter(status='Disponível')
    return render(request, 'listar_doacoes.html', {'doacoes': doacoes})


def listar_instituicoes(request):
    """ Lista de todas as instituições cadastradas """
    instituicoes = Instituicao.objects.all()
    return render(request, 'listar_instituicoes.html', {'instituicoes': instituicoes})


def listar_necessidades(request):
    """ Lista de todas as necessidades aprovadas """
    necessidades = Necessidade.objects.filter(aprovado_por_admin=True)
    return render(request, 'listar_necessidades.html', {'necessidades': necessidades})


def detalhes_doacao(request, doacao_id):
    """ Detalhes de uma doação específica """
    doacao = get_object_or_404(Doacao, id=doacao_id)
    return render(request, 'detalhes_doacao.html', {'doacao': doacao})


def detalhes_instituicao(request, instituicao_id):
    """ Página pública de uma instituição """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    necessidades = Necessidade.objects.filter(instituicao=instituicao, aprovado_por_admin=True)
    return render(request, 'detalhes_instituicao.html', {'instituicao': instituicao, 'necessidades': necessidades})
