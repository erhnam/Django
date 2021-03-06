from django.conf.urls import patterns, include, url
from viajes import views
from .views import *

urlpatterns = [
	
	#Destinos
	url (r'^verDestino', views.verDestino, name='Ver Destinos'),
	url (r'^detalleDestino/(?P<destino_id>\d+)', views.detalleDestino, name='Detalles Destino'),
	url (r'^addDestino', views.addDestino, name='Anadir Destino'),

	#Viajes
	url (r'^verViajes', views.verViajes, name='Ver Viajes'),
	url (r'^addViaje', views.addViaje, name='Anadir Viaje'),
	url (r'^detalleViaje/(?P<viaje_id>\d+)', views.detalleViaje, name='Detalles de Viaje'),
	url (r'^editarViaje/(?P<viaje_id>\d+)$', views.editarViaje, name='Editar Viaje'),

	#Usuarios
	url (r'login/$', views.login, name='login'),

	#Rutas (con Vistas basadas en clases)
	url (r'^verRuta', verRuta.as_view(), name='Ver Ruta'),
	url (r'^addRuta', addRuta.as_view(), name='Anadir Ruta'),
	url (r'^detalleRuta/(?P<Ruta_id>\w+)$', detalleRuta.as_view(), name='Detalles Ruta'),
]