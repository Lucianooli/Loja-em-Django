# Generated by Django 5.0.7 on 2024-07-23 22:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_principal', '0012_delete_subcategoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('Categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategoria', to='sistema_principal.categoria')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='subcategoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='sistema_principal.subcategoria'),
            preserve_default=False,
        ),
    ]
