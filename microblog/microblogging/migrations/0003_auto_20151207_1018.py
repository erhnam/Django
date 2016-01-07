# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblogging', '0002_auto_20151207_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='seguidores',
            field=models.ManyToManyField(related_name='seguido_por', to='microblogging.UserProfile', blank=True),
        ),
    ]
