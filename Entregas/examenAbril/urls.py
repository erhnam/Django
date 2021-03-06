from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from Entregas import views
from Entregas.views import verRuta


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'examenAbril.views.home', name='home'),
    # url(r'^examenAbril/', include('examenAbril.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', TemplateView.as_view (template_name = 'index.html'),name='index'),
    url(r'^Entregas/', include ('Entregas.urls', namespace = 'Entregas')),
    url(r'^admin/', include(admin.site.urls)),
    url (r'^login', views.userLogin, name='Login'),
    url (r'^logout', views.userLogout, name='Logout'),

   
)
