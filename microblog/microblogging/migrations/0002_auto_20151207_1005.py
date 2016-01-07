# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblogging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='difundir',
            name='relacion_difusiones',
            field=models.ManyToManyField(related_name='difundido_por', to='microblogging.UserProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='relacion_favoritos',
            field=models.ManyToManyField(related_name='favorito_de', to='microblogging.UserProfile', blank=True),
        ),
    ]
