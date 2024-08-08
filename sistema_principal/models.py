from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class SubCategoria(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, related_name='produtos', on_delete=models.CASCADE)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_de_produtos = models.IntegerField()  # Usar IntegerField para quantidade
    
    def valortotal(self):
        return self.preco - self.desconto

    def __str__(self):
        return self.nome

    def primeira_imagem(self):
        return self.imagens.first() if self.imagens.exists() else None

class Promocao(models.Model):
    nome = models.CharField(max_length=100)
    produtos = models.ManyToManyField(Produto, related_name='promocoes')
    # Outras informações da promoção, como data de início e fim, etc.

    def __str__(self):
        return self.nome

class ImagemProduto(models.Model):
    produto = models.ForeignKey('Produto', related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/imagens/')

    def __str__(self):
        return f'Imagem de {self.produto.nome}'
        
class Carrinho(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usa o modelo de usuário configurado
    produtos = models.ManyToManyField(Produto, through='ItemCarrinho')
    
    def __str__(self):
        return f'Carrinho de {self.usuario}'

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE)  # Removido null e blank
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tamanho = models.CharField(max_length=10, blank=True, null=True)  # Adicionando o campo tamanho


    def subtotal(self):
        return self.quantidade * self.produto.valortotal()

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} no carrinho de {self.carrinho.usuario}'

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('em_processamento', 'Em processamento'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    endereco_entrega = models.CharField(max_length=255)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='em_processamento')
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def valor_total(self):
        itens = ItemPedido.objects.filter(pedido=self)
        total = sum(item.produto.valortotal() * item.quantidade for item in itens)
        return total + self.valor_frete

    def __str__(self):
        return f'Pedido {self.id} de {self.usuario}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} no pedido {self.pedido.id}'

class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='favoritos')

    class Meta:
        unique_together = ('usuario', 'produto')  # Garante que um usuário só pode favoritar um produto uma vez

    def __str__(self):
        return f"{self.usuario.username} - {self.produto.nome}"
