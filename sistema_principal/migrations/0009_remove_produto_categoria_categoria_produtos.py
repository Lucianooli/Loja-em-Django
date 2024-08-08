# Generated by Django 5.0.7 on 2024-07-23 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_principal', '0008_alter_produto_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='categoria',
        ),
        migrations.AddField(
            model_name='categoria',
            name='produtos',
            field=models.ManyToManyField(related_name='categorias', to='sistema_principal.produto'),
        ),
    ]