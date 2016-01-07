# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lugar', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('distancia', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre_Ruta', models.CharField(max_length=100)),
                ('Precio_total', models.IntegerField()),
                ('Duracion_Total', models.IntegerField()),
                ('Destinos', models.ManyToManyField(to='viajes.Destino')),
            ],
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero_de_dias', models.IntegerField()),
                ('coste', models.IntegerField()),
                ('modo_desplazamiento', models.CharField(max_length=100)),
                ('destino', models.ForeignKey(to='viajes.Destino')),
            ],
        ),
    ]
