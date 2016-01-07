# -*- encoding: utf-8 -*- 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.views.generic import TemplateView

# Create your views here.

#destinos

def verDestino (request):
	destinos = Destino.objects.all()
	return render(request, 'verDestino.html', {'context': context,})

def detalleDestino (request, destino_id):
	destino = Destino.objects.get(pk=destino_id)
	return render(request, 'detalleDestino.html',{'destino': destino})

def addDestino(request):
	if request.method == 'POST' :
		destino = Destino()
		form = DestinoForm (request.POST, instance = destino)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else :
		form = DestinoForm()
	return render_to_response ('addDestino.html', {'form':form}, context_instance = RequestContext(request))

#Viajes

def verViajes (request):
	viajes = Viaje.objects.all()
	return render(request, 'verViajes.html', {'viajes': viajes})

def addViaje(request):
	if request.method == 'POST' :
		viaje = Viaje()
		form = ViajeForm (request.POST, instance = viaje)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else :
		form = ViajeForm()
	return render_to_response ('addViaje.html', {'form':form}, context_instance = RequestContext(request))

def detalleViaje (request, viaje_id):
	viaje = Viaje.objects.get(pk=viaje_id)
	return render(request,'detalleViaje.html',{'viaje': viaje})

def editarViaje(request, viaje_id):
	viaje = Viaje.objects.get(pk = viaje_id)
	if request.method == 'POST':
		form = ViajeForm(request.POST, instance = viaje)
		if form.is_valid():
			form.save()
           	return HttpResponseRedirect('/')
	else:
		form = ViajeForm(instance = viaje)
        return render_to_response('editarViaje.html', {'form': form}, context_instance=RequestContext(request) )

#Usuarios
def Login(request):
    # Si el usuario esta ya logueado, lo redireccionamos a home
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                pass
   		mensaje = 'Nombre de usuario o contraseña no valido'
    return render(request,'login.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/login')
def Logout(request):
    logout(request)
    return redirect('/')

#Rutas (con Vistas basadas en clases)

class verRuta(View):
    template_name = 'verRuta.html'
    def get(self, request, *args, **kwargs):
        rutas = Ruta.objects.all()
        return render(request, self.template_name, {'rutas':rutas})


class addRuta(View):
    form_class = RutaForm
    template_name = 'addRuta.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()        
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():    
            form.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class detalleRuta(View):
    template_name = 'detalleRuta.html'

    def get(self, request, *arg, **kwargs):
        id = self.kwargs['Ruta_id']
        ruta = get_object_or_404(Ruta, pk = id)     
        return render(request,self.template_name,{'rutaDetalle':ruta,'user':request.user})

