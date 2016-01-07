# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Difundir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rumor',
            fields=[
                ('rumor_id', models.AutoField(serialize=False, primary_key=True)),
                ('contenido', models.CharField(max_length=140)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('num_favorito', models.IntegerField(default=0)),
                ('num_difusion', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name='user_profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('photo', models.ImageField(null=True, upload_to=b'profiles', blank=True)),
                ('seguidores', models.ManyToManyField(related_name='seguido_por', null=True, to='microblogging.UserProfile', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='rumor',
            name='username',
            field=models.ForeignKey(to='microblogging.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='favorito',
            name='relacion_favoritos',
            field=models.ManyToManyField(related_name='favorito_de', null=True, to='microblogging.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='favorito',
            name='rumor_id',
            field=models.ForeignKey(to='microblogging.Rumor'),
        ),
        migrations.AddField(
            model_name='difundir',
            name='relacion_difusiones',
            field=models.ManyToManyField(related_name='difundido_por', null=True, to='microblogging.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='difundir',
            name='rumor_id',
            field=models.ForeignKey(to='microblogging.Rumor'),
        ),
    ]
