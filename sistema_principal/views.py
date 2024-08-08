from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProdutoForm, PedidoForm
from .models import Produto, Categoria, Carrinho, Favorito, ItemCarrinho
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse
import uuid
from django.core.mail import send_mail
from .forms import CheckoutForm
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import stripe
import pdfkit
from .models import Pedido
from django.template.loader import render_to_string
from .utils import gerar_boleto  # Certifique-se de que o arquivo utils.py está presente
from django.http import HttpResponse




stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    produto_brinco = Produto.objects.get(id=14)
    return render(request, 'sistema_principal/inicio.html', {
        'produtos': produtos,
        'categorias': categorias,
        'produto_brinco': produto_brinco
    })

class LogoutGetView(View):
    def get(self, request):
        logout(request)
        return redirect('inicio')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserRegistrationForm()
    return render(request, 'sistema_principal/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Você foi logado com sucesso.')
            return redirect('inicio')  # Redireciona para a página inicial após o login
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'sistema_principal/login.html', {'form': form})

def produto_detalhes(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'sistema_principal/produto_detalhes.html', {'produto': produto})

def categoria_view(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    produtos = Produto.objects.filter(categoria=categoria)  # Filtra produtos pela categoria
    return render(request, 'sistema_principal/categoria.html', {'categoria': categoria, 'produtos': produtos})

def pesquisar(request):
    query = request.GET.get('q')
    produtos = Produto.objects.filter(nome__icontains=query) if query else Produto.objects.all()
    return render(request, 'sistema_principal/pesquisa_resultados.html', {'produtos': produtos, 'query': query})

def carrinho(request):
    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    if not carrinho:
        produtos = []
        valor_total = 0
    else:
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
        produtos = []

        for item in itens_carrinho:
            produto = item.produto
            valortotal = produto.valortotal() if callable(produto.valortotal) else produto.valortotal
            produtos.append({
                'produto': produto,
                'quantidade': item.quantidade,
                'tamanho': item.tamanho,
                'subtotal': valortotal * item.quantidade,
                'item_id': item.id
            })

        valor_total = sum(item['subtotal'] for item in produtos)

    return render(request, 'sistema_principal/carrinho.html', {'produtos': produtos, 'valor_total': valor_total})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))  # Default para 1 se não fornecido
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
    tamanho = request.POST.get('tamanho')  # Pegue o tamanho do POST
    
    # Tenta obter o item do carrinho existente
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto, tamanho=tamanho).first()
    
    if item_carrinho:
        # Se o item já existir no carrinho, atualize a quantidade
        item_carrinho.quantidade += quantidade
        item_carrinho.save()
    else:
        # Se o item não existir, crie um novo
        item_carrinho = ItemCarrinho(carrinho=carrinho, produto=produto, quantidade=quantidade, tamanho= tamanho    )
        item_carrinho.save()
    
    return redirect('carrinho')  # Redireciona para a página do carrinho

@login_required
def adicionar_remover_favorito(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    favorito, criado = Favorito.objects.get_or_create(usuario=request.user, produto=produto)

    if not criado:
        # Se já existia, remove (desfavorita)
        favorito.delete()

    return redirect('lista_favoritos')

def lista_favoritos(request):
    # Obtém os produtos favoritos do usuário logado
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('produto')
    return render(request, 'sistema_principal/lista_favoritos.html', {'favoritos': favoritos})

def remover_item(request, produto_id):
    try:
        # Supondo que você tenha uma maneira de identificar o carrinho do usuário
        carrinho = Carrinho.objects.get(usuario=request.user)
        
        # Obter todos os itens do carrinho que correspondem ao produto_id
        itens = ItemCarrinho.objects.filter(carrinho=carrinho, produto_id=produto_id)
        
        # Remover todos os itens
        count, _ = itens.delete()
        
        if count > 0:
            messages.success(request, 'Item(s) removido(s) com sucesso!')
        else:
            messages.error(request, 'Nenhum item encontrado para remoção.')

    except Carrinho.DoesNotExist:
        messages.error(request, 'Carrinho não encontrado.')
    except Exception as e:
        messages.error(request, f'Erro: {e}')

    return redirect('carrinho')



def gerar_nota_fiscal(endereco, charge):
    context = {
        'endereco': endereco,
        'charge': charge,
        'valor_total': charge['amount'] / 100,  # valor em reais
    }
    html_content = render_to_string('sistema_principal/nota_fiscal.html', context)
    pdf = pdfkit.from_string(html_content, False)

    send_mail(
        'Sua Nota Fiscal',
        'Segue em anexo a sua nota fiscal.',
        settings.DEFAULT_FROM_EMAIL,
        [charge['receipt_email']],
        fail_silently=False,
        html_message=html_content,
        attachments=[('nota_fiscal.pdf', pdf, 'application/pdf')]
    )


def gerar_boleto(endereco):
    # Aqui você vai gerar o boleto e armazená-lo em um local acessível
    boleto_url = 'http://exemplo.com/boleto'  # Atualize com a URL real
    return boleto_url

def criar_pedido(request):
    # Exemplo de criação de um pedido e definição do ID na sessão
    pedido = Pedido.objects.create(
        usuario=request.user,
        endereco='Algum endereço',
        valor_total=100.00,  # Valor total do pedido
    )
    request.session['pedido_id'] = pedido.id
    return redirect('checkout')


def gerar_chave_pix():
    # Lógica para gerar uma chave Pix real
    return '1234-5678-90'  # Exemplo de chave Pix

@login_required
def finalizar_compra(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Aqui você pode fazer alguma validação adicional, se necessário
            return redirect('checkout')  # Redirecionar para a página de checkout
    else:
        form = PedidoForm()
    return render(request, 'sistema_principal/finalizar_compra.html', {'form': form})

def checkout(request):
    if request.method == 'POST':
        endereco = request.POST.get('endereco')
        pagamento = request.POST.get('pagamento')
        stripe_token = request.POST.get('stripeToken')
        
        if pagamento == 'pix':
            # Processar o pagamento via Pix
            return redirect('confirmar_pedido', status='pix', endereco=endereco)
        elif pagamento in ['credito', 'debito']:
            # Processar o pagamento via Stripe
            try:
                charge = stripe.Charge.create(
                    amount=1000,  # valor em centavos
                    currency='brl',
                    description='Descrição do pedido',
                    source=stripe_token,
                )
                if charge['paid']:
                    return redirect('confirmar_pedido', status='aprovado', endereco=endereco)
                else:
                    return redirect('confirmar_pedido', status='rejeitado', endereco=endereco)
            except stripe.error.CardError as e:
                return HttpResponse('Erro ao processar pagamento: {}'.format(e))
        else:
            return HttpResponse('Método de pagamento inválido')

    return render(request, 'sistema_principal/checkout.html', {'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'invalid signature'}, status=400)

    if event['type'] == 'charge.succeeded':
        charge = event['data']['object']
        # Verifique se o pedido correspondente existe e atualize o status
        try:
            pedido = Pedido.objects.get(charge_id=charge['id'])
            pedido.status = 'confirmado'
            pedido.save()
        except Pedido.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'}, status=200)

def pedido_confirmado(request):
    return render(request, 'sistema_principal/pedido_confirmado.html')

def confirmar_pedido(request, status, endereco):
    if status == 'pix':
        mensagem = "Aguarde a confirmação do pagamento via Pix."
    elif status == 'aprovado':
        mensagem = "Pagamento aprovado! Seu pedido foi confirmado."
    elif status == 'rejeitado':
        mensagem = "Pagamento rejeitado. Por favor, tente novamente."
    else:
        mensagem = "Compra inválida. O pedido foi cancelado."

    return render(request, 'sistema_principal/confirmar_pedido.html', {'mensagem': mensagem, 'endereco': endereco})


