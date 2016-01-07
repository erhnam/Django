# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destinatario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=128)),
                ('direccion', models.CharField(max_length=128)),
                ('ciudad', models.CharField(max_length=128)),
                ('codigo_postal', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.CharField(max_length=128)),
                ('valor', models.IntegerField()),
                ('destinatarioReceptor', models.ForeignKey(to='Entregas.Destinatario')),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombredelaruta', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200, blank=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('paquete', models.ForeignKey(to='Entregas.Paquete')),
            ],
        ),
    ]
