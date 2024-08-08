from django.contrib import admin
from .models import Produto, ImagemProduto, Categoria, SubCategoria, Promocao

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'subcategoria', 'preco', 'quantidade_de_produtos')
    list_filter = ('categoria', 'subcategoria')
    search_fields = ('nome', 'descricao')
    inlines = [ImagemProdutoInline]  # Adiciona o inline ao admin de Produto


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome',)

class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    filter_horizontal = ('produtos',)  # Adiciona um widget de seleção para o campo many-to-many

admin.site.register(Categoria)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Promocao, PromocaoAdmin)
admin.site.register(ImagemProduto)