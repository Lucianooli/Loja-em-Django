# Generated by Django 5.0.7 on 2024-08-02 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_principal', '0020_favorito'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(default=1, upload_to='produtos/imagens/'),
            preserve_default=False,
        ),
    ]