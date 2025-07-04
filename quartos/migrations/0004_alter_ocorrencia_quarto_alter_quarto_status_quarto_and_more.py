# Generated by Django 5.1.7 on 2025-05-23 00:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quartos', '0003_quarto_reserva_liberada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocorrencia',
            name='quarto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='quartos.quarto'),
        ),
        migrations.AlterField(
            model_name='quarto',
            name='status_quarto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='quartos.statusquarto'),
        ),
        migrations.AlterField(
            model_name='quarto',
            name='tipo_quarto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='quartos.tipoquarto'),
        ),
        migrations.AlterField(
            model_name='tarifatipoquarto',
            name='tipo_quarto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='quartos.tipoquarto'),
        ),
    ]
