# Generated by Django 5.0.7 on 2024-08-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_principal', '0026_alter_itemcarrinho_carrinho_alter_pedido_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcarrinho',
            name='tamanho',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]