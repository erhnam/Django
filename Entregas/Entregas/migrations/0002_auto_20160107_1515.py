# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Entregas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinatario',
            name='ciudad',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='destinatario',
            name='codigo_postal',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='destinatario',
            name='direccion',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='destinatario',
            name='nombre',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='contenido',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='destinatarioReceptor',
            field=models.ForeignKey(to='Entregas.Destinatario', null=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='valor',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='descripcion',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='nombredelaruta',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='paquete',
            field=models.ForeignKey(to='Entregas.Paquete', null=True),
        ),
    ]
