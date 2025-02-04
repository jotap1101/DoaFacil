from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['item', 'descricao', 'estado_conservacao', 'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'estado_conservacao': forms.Select(),
            'status': forms.Select(),
}
        
class EditDoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['item', 'descricao', 'estado_conservacao', 'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'estado_conservacao': forms.Select(),
            'status': forms.Select(),
}


class NecessidadeForm(forms.ModelForm):
    class Meta:
        model = Necessidade
        fields = ['item', 'descricao', 'quantidade', 'aprovado_por_admin', 'status']

class UsuarioCadastroForm(UserCreationForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.exclude(nome="Administrador"), 
        label="Tipo de Usuário")

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'email','tipo_usuario']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'categoria', 'descricao', 'status']

