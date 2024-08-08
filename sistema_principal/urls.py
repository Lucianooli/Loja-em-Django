from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import remover_item,confirmar_pedido

urlpatterns = [
    path('', views.index, name='inicio'),
    path('registrar/', views.register, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.LogoutGetView.as_view(), name='logout'),
    path('produto/<int:produto_id>/', views.produto_detalhes, name='produto_detalhes'),
    path('categoria/<int:categoria_id>/', views.categoria_view, name='categoria'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('favoritos/adicionar/<int:produto_id>/', views.adicionar_remover_favorito, name='adicionar_remover_favorito'),
    path('favoritos/', views.lista_favoritos, name='lista_favoritos'),
    path('carrinho/remover/<int:produto_id>/', views.remover_item, name='remover_item'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('pedido-confirmado/', views.pedido_confirmado, name='pedido_confirmado'),  # Crie essa view e template para confirmação
    path('checkout/', views.checkout, name='checkout'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('confirmar-pedido/<str:status>/<str:endereco>/', confirmar_pedido, name='confirmar_pedido'),


]

# Adiciona URL para arquivos estáticos e de mídia apenas se DEBUG estiver ativado
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
