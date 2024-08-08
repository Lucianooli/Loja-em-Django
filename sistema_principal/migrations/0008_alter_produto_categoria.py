# Generated by Django 5.0.7 on 2024-07-23 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_principal', '0007_remove_categoria_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='sistema_principal.categoria'),
        ),
    ]
