# Generated by Django 5.0.7 on 2024-07-24 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_principal', '0015_produto_categoria_produto_quantidade_de_produtos'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='produtos/imagens/')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='sistema_principal.produto')),
            ],
        ),
    ]
