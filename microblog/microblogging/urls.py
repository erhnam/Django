from django.conf.urls import url
from . import views
from microblogging import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'contacto$', views.contacto, name='contacto'),
	url(r'sobre_mi$', views.sobre_mi, name='sobre_mi'),	
	url(r'gracias/(?P<username>[\w]+)/(?P<login>[\w]+)/$',views.gracias, name='gracias'),
	url(r'registro/$', views.registro, name='registro'),
	url(r'login/$', views.login, name='login'),
	url(r'eliminar_cuenta/$', views.eliminar_cuenta, name='eliminar_cuenta'),
	url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': 'home'} ),		
	url(r'editar_email/$', views.editar_email, name='editar_email'),
	url(r'editar_contrasena/$', views.editar_contrasena, name='editar_contrasena'),
	url(r'editar_foto/$', views.editar_foto, name='editar_foto'),	
	url(r'usuario/(?P<username>\w+)/(?P<username1>\w+)/$', views.usuario, name='usuario'),
	url(r'seguir/(?P<username>[\w]+)/$', views.seguir, name='seguir'),
	url(r'buscar/$', views.buscar, name='buscar'),
	url(r'dejar/(?P<username>[\w]+)/$', views.dejar, name='dejar'),
	url(r'fav/(?P<user_id>\w+)/(?P<rumor_id>\d+)/$', views.fav, name='fav'),
	url(r'difundir/(?P<user_id>\w+)/(?P<rumor_id>\d+)/$', views.difundir, name='fav'),
	url(r'borrar/(?P<rumor_id>\d+)/$', views.borrarRumor, name='borrar'),
	url(r'seguidores/$', views.seguidores, name='seguidores'),
	url(r'siguiendo_a/$', views.siguiendo_a, name='siguiendo_a'),
]