from django import forms
from .models import Doacao, Necessidade

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['nome', 'descricao', 'categoria', 'estado_conservacao']

class NecessidadeForm(forms.ModelForm):
    class Meta:
        model = Necessidade
        fields = ['descricao', 'quantidade']
