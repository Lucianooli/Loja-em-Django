from typing import Any
from django import forms
from .models import Produto, Pedido, ItemPedido, ImagemProduto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'categoria', 'subcategoria', 'desconto', 'quantidade_de_produtos']

class ImagemProdutoForm(forms.ModelForm):
    class Meta:
        model = ImagemProduto
        fields = ['produto', 'imagem']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['endereco_entrega', 'status', 'valor_frete']

    

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome',
            'password1': 'Senha',
            'password2': 'Confirma senha',
        }
        error_messages = {
            'username': {
                'required': 'Este campo é obrigatório.',
            },
            'email': {
                'required': 'O e-mail é obrigatório.',
            },
            'password1': {
                'required': 'A senha é obrigatória.',
                'password_too_short': 'A senha é muito curta. Deve conter pelo menos 8 caracteres.',  # Custom message
                'password_entirely_numeric': 'A senha não pode ser inteiramente numérica.',  # Custom message
            },
            'password2': {
                'required': 'A confirmação da senha é obrigatória.',
                'password_mismatch': 'A senha não corresponde com a anterior.',
            },
        }
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Digite a senha'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirme a senha'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover dicas e mensagens padrão do formulário
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    


class CheckoutForm(forms.Form):
    endereco = forms.CharField(max_length=255, required=True, label='endereço de entrega')
    # Outros campos necessários    metodo_pagamento = forms.ChoiceField(choices=[('cartao', 'Cartão de Crédito'), ('boleto', 'Boleto')], label='Método de Pagamento')