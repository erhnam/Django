from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
	
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, related_name='user_profile')
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)
    seguidores=models.ManyToManyField('self', blank=True, related_name='seguido_por', symmetrical=False)

    def __unicode__(self):
        return self.user.username

class Rumor(models.Model):
	rumor_id = models.AutoField(primary_key=True)
	username = models.ForeignKey(UserProfile, null=True)
	contenido = models.CharField(max_length=140, unique=False)
	fecha = models.DateTimeField(auto_now_add=True)
	num_favorito = models.IntegerField(default=0)
	num_difusion = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.contenido

class Favorito(models.Model):
	rumor_id = models.ForeignKey(Rumor)
	relacion_favoritos = models.ManyToManyField(UserProfile, blank=True, related_name='favorito_de', symmetrical=False)
	
class Difundir(models.Model):
	rumor_id = models.ForeignKey(Rumor)
	relacion_difusiones = models.ManyToManyField(UserProfile, blank=True, related_name='difundido_por', symmetrical=False)
