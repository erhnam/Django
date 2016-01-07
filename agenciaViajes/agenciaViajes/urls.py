from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from viajes import views
from viajes.views import verDestino

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('viajes.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^viajes/', include ('viajes.urls', namespace = 'viajes')),
    url (r'^login', views.Login, name='Login'),
    url (r'^logout', views.Logout, name='Logout'),
]