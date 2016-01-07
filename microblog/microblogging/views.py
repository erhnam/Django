# -*- encoding: utf-8 -*- 
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required   #para loguin
from .forms import RegistroUserForm, EditarEmailForm, EditarContrasenaForm, RumorNewForm, EditarFotoForm, ContactNewForm
from .models import UserProfile, Rumor, Favorito, Difundir
from django.contrib import auth                             #para arreglar error de login() takes exactly 1 argument (2 given)
from django.contrib.auth import authenticate, login, logout #para logout y login                                                    
from django.contrib.auth.hashers import make_password       #para password                                                            
from random import sample                                   #Para usar el random
from itertools import chain                                 #Une varios objetos en lista
from operator import attrgetter                             #Ordena la lista por un campo del Objeto.
from django.contrib import messages                         #para mostrar mensajes

#mostrar pagina principal con rumores con modal
@login_required
def home(request):    
    #para los rumores
    if request.method == 'POST':
        form = RumorNewForm(data=request.POST)
        if form.is_valid():
            try:
                user_model=UserProfile.objects.get(user=request.user)
            except request.user.DoesNotExist:
                user_model = None
            Rumor.objects.create(contenido=form.cleaned_data['texto'], username=user_model)
            nuevo = Rumor.objects.filter(contenido=form.cleaned_data['texto'], username=user_model)
            return HttpResponseRedirect('/')
    else:
        form = RumorNewForm()

    #para la persona
    try:
        UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/logout')

    q=UserProfile.objects.get(user=request.user)
    p=UserProfile.objects.filter(seguidores=q)
    #personas sugeridas para seguir
    todos=sugeridos(request)
    #Rumores de la persona principal
    rumorespropios=Rumor.objects.filter(username=q)   
    #Rumores de las personas a las que se sigue                                      
    rumores=Rumor.objects.filter(username=p).order_by('-fecha')
    #Rumores de mios y los seguidores ordenados de mas nuevos a mas viejos.
    rumores = sorted(chain(rumorespropios, rumores),key=attrgetter('fecha'),reverse=True)   
    return render(request, 'home.html', {'form': form, 'Rumores':rumores, 'siguiendo':p, 'seguido':q, 'elegidos':todos,})

#muestra los seguidores
def seguidores(request):
    #para los rumores
    if request.method == 'POST':
        form = RumorNewForm(data=request.POST)
        if form.is_valid():
            try:
                user_model=UserProfile.objects.get(user=request.user)
            except request.user.DoesNotExist:
                user_model = None
            Rumor.objects.create(contenido=form.cleaned_data['texto'], username=user_model)
            nuevo = Rumor.objects.get(contenido=form.cleaned_data['texto'], username=user_model)
            return HttpResponseRedirect('/')
    else:
        form = RumorNewForm()
    #para los seguidores y seguidos    
    try:
        UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/logout')

    q=UserProfile.objects.get(user=request.user)
    p=UserProfile.objects.filter(seguidores=q)
    return render(request, 'seguidores.html', {'form': form, 'siguiendo':p, 'seguido':q,})

#muestra a quien sigue
def siguiendo_a(request):
    #para los rumores
    if request.method == 'POST':
        form = RumorNewForm(data=request.POST)
        if form.is_valid():
            try:
                user_model=UserProfile.objects.get(user=request.user)
            except request.user.DoesNotExist:
                user_model = None
            Rumor.objects.create(contenido=form.cleaned_data['texto'], username=user_model)
            nuevo = Rumor.objects.get(contenido=form.cleaned_data['texto'], username=user_model)
            return HttpResponseRedirect('/')
    else:
        form = RumorNewForm()

    #para los seguidores y seguidos    
    try:
        UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/logout')
    q=UserProfile.objects.get(user=request.user)
    p=UserProfile.objects.filter(seguidores=q)
    return render(request, 'siguiendo_a.html', {'form': form, 'siguiendo':p, 'seguido':q,})

#Contactar conmigo
def contacto(request):
    usuario=User.objects.get(username=request.user.username)
    username=usuario.username
    if request.method == 'POST':
        form = ContactNewForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            texto = form.cleaned_data['texto']
            login='2'
            return redirect(reverse('gracias', kwargs={'username': username, 'login': login}))
    else:
        form = ContactNewForm()
    return render(request, 'contacto.html', {'form': form, })


#sobre mi

def sobre_mi(request):
    return render(request, 'sobre_mi.html')

#registrar usuario
def registro(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RegistroUserForm(request.POST, request.FILES)

        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el username del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            # E instanciamos un objeto User, con el username y password
            user_model = User.objects.create_user(username=username, password=password)
            # Anadimos el email
            user_model.email = email
            # Y guardamos el objeto, esto guardara los datos en la db.
            user_model.save()
            # Ahora, creamos un objeto UserProfile, aunque no haya incluido
            # una imagen, ya quedara la referencia creada en la db.
            user_profile = UserProfile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            # y le asignamos la photo (el campo, permite datos null)
            user_profile.photo = photo
            # Por ultimo, guardamos tambien el objeto UserProfile
            user_profile.save()
            # Ahora, redireccionamos a la pagina gracias.html
            # Pero lo hacemos con un redirect.
            login='1'
            return redirect(reverse('gracias', kwargs={'username': username, 'login': login}))
    else:
        # Si el method es GET, instanciamos un objeto RegistroUserForm vacio
        form = RegistroUserForm()
    # Creamos el concontenido
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'registro.html', context)

def gracias(request, username, login):
    return render(request, 'gracias.html', {'username': username, 'login': login})    

#dar de baja a un usuario
@login_required
def eliminar_cuenta(request):
    usuario=User.objects.get(username=request.user.username)
    username=usuario.username
    usuario.delete()
    login='0'
    return redirect(reverse('gracias', kwargs={'username': username, 'login':login}))

# para loguear al usuario
def login(request):
    # Si el usuario esta ya logueado, lo redireccionamos a home
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect(reverse('home'))
            else:
                pass
        mensaje = 'Nombre de usuario o contraseña no valido'
    return render(request, 'login.html', {'mensaje': mensaje})

#desloguear usuario
@login_required
def logout(request):
    logout(request)
    return redirect('/')

#editar email
@login_required
def editar_email(request):
    q=UserProfile.objects.get(user=request.user)    
    if request.method == 'POST':
        form = EditarEmailForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'El email ha sido cambiado con exito!.')
            return render(request, 'editar_email.html', {'form': form, 'seguido': q}) 
    else:
        form = EditarEmailForm(
            request=request,
            initial={'email': request.user.email})
    return render(request, 'editar_email.html', {'form': form, 'seguido': q})

#editar contraseña
@login_required
def editar_contrasena(request):
    q=UserProfile.objects.get(user=request.user)    
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, 'La contraseña ha sido cambiado con exito!.')
            messages.success(request, 'Es necesario introducir los datos para entrar.')
            return render(request, 'editar_contrasena.html', {'form': form, 'seguido': q}) 
    else:
        form = EditarContrasenaForm()
    return render(request, 'editar_contrasena.html', {'form': form, 'seguido': q})    

#editar foto
@login_required
def editar_foto(request):
    if request.method == 'POST':
        form = EditarFotoForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.user_profile.photo = form.cleaned_data['imagen']
            request.user.user_profile.save()
            return render(request, 'editar_foto.html', {'form': form, 'seguido': request.user.user_profile})
    else:
        form = EditarFotoForm()
    return render(request, 'editar_foto.html', {'form': form, 'seguido': request.user.user_profile}) 

#sugiere a quien seguir
@login_required
def sugeridos(request):
    usuario=User.objects.get(username=request.user.username)
    q=UserProfile.objects.get(user=request.user)
    p=UserProfile.objects.filter(seguidores=q)
    contador=UserProfile.objects.all().count()
    rand_ids=sample(xrange(1, contador), 4)
    final=UserProfile.objects.filter(pk__in=rand_ids).exclude(seguidores=q).exclude(user=usuario)
    return final

#cuenta del usuario
def usuario(request,username,username1):
    #para los rumores
    if request.method == 'POST':
        form = RumorNewForm(data=request.POST)
        if form.is_valid():
            try:
                user_model=UserProfile.objects.get(user=request.user)
            except request.user.DoesNotExist:
                user_model = None
            Rumor.objects.create(contenido=form.cleaned_data['texto'], username=user_model)
            nuevo = Rumor.objects.filter(contenido=form.cleaned_data['texto'], username=user_model)
            return HttpResponseRedirect('/')
    else:
        form = RumorNewForm()    
    usuario=User.objects.get(username=username1)
    usuario=UserProfile.objects.filter(seguidores=usuario.user_profile)
    p=User.objects.get(username=username1)
    encontrado=User.objects.get(username=username) 
    q=UserProfile.objects.get(user=encontrado.user_profile.user)
    seguido=False
    #busco si sigo a la persona
    for x in usuario:
        if x==p.user_profile:
            seguido=True    
    usuario=UserProfile.objects.get(user=encontrado)
    usuario=UserProfile.objects.filter(seguidores=usuario)
    #personas sugeridas para seguir
    todos=sugeridos(request)
    buscado=User.objects.get(username=username)            #sacamos de la base de datos al usuario
    buscado=UserProfile.objects.get(user=buscado)
    siguiendo=UserProfile.objects.filter(seguidores=buscado)    #a los que ella sigue
    rumores=Rumor.objects.filter(username=buscado).order_by('-fecha')
    usuario=UserProfile.objects.get(user=request.user)
    seguidoresusuario=UserProfile.objects.filter(seguidores=request.user.user_profile)
    return render(request, 'buscar.html',{"form":form, "seguido":seguido, "Rumores":rumores, "seguidoresusuario":seguidoresusuario, "usuario": usuario, "Usuarios":siguiendo, "siguiendo":q, "Seguidme":encontrado, "sugeridos": todos})

#buscar usuarios
@login_required
def buscar(request):
        #para los rumores
    if request.method == 'POST':
        form = RumorNewForm(data=request.POST)
        if form.is_valid():
            try:
                user_model=UserProfile.objects.get(user=request.user)
            except request.user.DoesNotExist:
                user_model = None
            Rumor.objects.create(contenido=form.cleaned_data['texto'], username=user_model)
            nuevo = Rumor.objects.filter(contenido=form.cleaned_data['texto'], username=user_model)
            return HttpResponseRedirect('/')
    else:
        form = RumorNewForm()

    consulta=request.GET.get('q', '')                           #creamos la consulta devolviendo un nombre
    try:
        encontrado=User.objects.get(username=consulta)          #localizamos al usuario a buscar
    except User.DoesNotExist:
        return HttpResponseRedirect('/')

    q=UserProfile.objects.get(user=encontrado.user_profile.user)
    p=UserProfile.objects.filter(seguidores=q)
    #buscamos a los seguidores del usuario principal
    usuario=UserProfile.objects.get(user=request.user)
    usuario=UserProfile.objects.filter(seguidores=usuario)
    #personas sugeridas para seguir
    todos=sugeridos(request)
    buscado=UserProfile.objects.get(user=encontrado)            #sacamos de la base de datos al usuario
    siguiendo=UserProfile.objects.filter(seguidores=buscado)    #a los que ella sigue
    rumores=Rumor.objects.filter(username=buscado).order_by('-fecha')
    usuario=UserProfile.objects.get(user=request.user)
    seguidoresusuario=UserProfile.objects.filter(seguidores=request.user.user_profile)
  
    seguido=False
    for x in seguidoresusuario:
        if x==buscado:
            seguido=True
    return render(request, 'buscar.html',{"form":form, "seguido":seguido, "Rumores":rumores, "seguidoresusuario":seguidoresusuario, "usuario": usuario, "Usuarios":siguiendo, "siguiendo":q, "Seguidme":encontrado, "sugeridos": todos})

#seguir a un usuario
@login_required
def seguir(request, username):
    usuario_a_seguir=User.objects.get(username=username) #usuario a seguir
    usuario_actual=UserProfile.objects.get(user=request.user)  #usuario actual
    try:
        UserProfile.objects.get(user=usuario_a_seguir, seguidores=usuario_actual)
    except UserProfile.DoesNotExist:
        if request.user != username:
            nativo=UserProfile.objects.get(user=usuario_a_seguir)
            nativo.seguidores.add(usuario_actual)
            nativo.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
        
    return HttpResponseRedirect('/')

#dejar de seguir a una persona
@login_required
def dejar(request, username):
    siguiendo=User.objects.get(username=username)               #extraemos Usuario a dejar de seguir
    siguiendo=UserProfile.objects.get(user=siguiendo)           #extraemos UserProfile=User a dejar de seguir
    tu=UserProfile.objects.get(user=request.user)               #extrae al usuario principal
    siguiendo.seguidores.remove(tu)                             
    siguiendo.save()
    return HttpResponseRedirect('/')

#hacer de un rumor favorito
@login_required
def fav(request, user_id, rumor_id):
    rumor_favorito=Rumor.objects.get(rumor_id=rumor_id)
    usuario_pulsa_favorito=UserProfile.objects.get(user=request.user)
    try:
        Favorito.objects.get(rumor_id=rumor_favorito, relacion_favoritos=usuario_pulsa_favorito)
    except Favorito.DoesNotExist:
        try:
            Favorito.objects.get(rumor_id=rumor_favorito)
        except Favorito.DoesNotExist:
            encontrar_original=Rumor.objects.filter(contenido=rumor_favorito.contenido).exclude(username=user_id)
            original=Rumor.objects.get(rumor_id=encontrar_original)
            try:
                Favorito.objects.get(rumor_id=original, relacion_favoritos=usuario_pulsa_favorito)
            except Favorito.DoesNotExist:
                #Si no existe crea un favorito
                agrega_favorito=Favorito.objects.create(rumor_id=original)
                agrega_favorito.relacion_favoritos.add(usuario_pulsa_favorito)
                agrega_favorito.save()
                #aumentamos en 1 el original
                original.num_favorito +=1
                original.save()
                #aumentamos en 1 el favorito
                rumor_favorito.num_favorito +=1
                rumor_favorito.save()
                return HttpResponseRedirect('/')

            #si exite elimina favorito
            elimina_favorito=Favorito.objects.filter(rumor_id=original)
            elimina_favorito.delete()
            original.num_favorito -=1
            original.save()
            rumor_favorito.num_favorito -=1
            rumor_favorito.save()
            return HttpResponseRedirect('/')  

        #Si no existe crea un favorito
        agrega_favorito=Favorito.objects.get(rumor_id=rumor_favorito)
        agrega_favorito.relacion_favoritos.add(usuario_pulsa_favorito)
        agrega_favorito.save();
        rumor_favorito.num_favorito +=1
        rumor_favorito.save()
        return HttpResponseRedirect('/')
    
    #Si no existe crea un favorito    
    elimina_favorito=Favorito.objects.get(rumor_id=rumor_favorito, relacion_favoritos=usuario_pulsa_favorito)
    elimina_favorito.relacion_favoritos.remove(usuario_pulsa_favorito)
    elimina_favorito.save()
    rumor_favorito.num_favorito -=1
    rumor_favorito.save()
    return HttpResponseRedirect('/')

#Difundir el rumor
@login_required
def difundir(request, user_id, rumor_id):
    rumor_a_difundir=Rumor.objects.get(rumor_id=rumor_id)
    usuario_que_pulsa_difundir=UserProfile.objects.get(user=request.user)
    try:
        Difundir.objects.get(rumor_id=rumor_a_difundir, relacion_difusiones=usuario_que_pulsa_difundir)
    except Difundir.DoesNotExist:
        try:
            Difundir.objects.get(rumor_id=rumor_a_difundir)
        except Difundir.DoesNotExist:
            encontrar_original=Rumor.objects.filter(contenido=rumor_a_difundir.contenido).exclude(username=user_id)
            original=Rumor.objects.get(rumor_id=encontrar_original)
            try:
                Difundir.objects.get(rumor_id=original, relacion_difusiones=usuario_que_pulsa_difundir)
            except Difundir.DoesNotExist:
                #Si no existe crea una difusion
                agrega_favorito=Difundir.objects.create(rumor_id=original)
                agrega_favorito.relacion_difusiones.add(usuario_que_pulsa_difundir)
                agrega_favorito.save()
                original.num_difusion +=1
                original.save()
                rumor_a_difundir.num_difusion +=1
                rumor_a_difundir.save()
                if(original.username != usuario_que_pulsa_difundir):
                    Rumor.objects.create(contenido=original.contenido, username=usuario_que_pulsa_difundir)
                    creado=Rumor.objects.filter(contenido=original.contenido, username=usuario_que_pulsa_difundir)
                    creado.num_difusion=original.num_difusion
                    creado.num_favorito=original.num_favorito
                    for i in creado:
                        i.save()
                return HttpResponseRedirect('/')
            elimina_Difundir=Difundir.objects.filter(rumor_id=original)
            elimina_Difundir.delete()
            original.num_difusion -=1
            original.save()
            rumor_a_difundir.num_difusion -=1
            rumor_a_difundir.save()
            eliminame=Rumor.objects.filter(contenido=original.contenido, username=usuario_que_pulsa_difundir)
            eliminame.delete()
            return HttpResponseRedirect('/')    
        agrega_Difundir=Difundir.objects.get(rumor_id=rumor_a_difundir)
        agrega_Difundir.relacion_difusiones.add(usuario_que_pulsa_difundir)
        agrega_Difundir.save();
        rumor_a_difundir.num_difusion +=1
        rumor_a_difundir.save()
        if(rumor_a_difundir.username != usuario_que_pulsa_difundir):
            Rumor.objects.create(contenido=rumor_a_difundir.contenido, username=usuario_que_pulsa_difundir)
            creado=Rumor.objects.get(contenido=rumor_a_difundir.contenido, username=usuario_que_pulsa_difundir)
            creado.num_difusion=rumor_a_difundir.num_difusion
            creado.num_favorito=rumor_a_difundir.num_favorito
            creado.save()
        return HttpResponseRedirect('/')
    elimina_Difundir=Difundir.objects.get(rumor_id=rumor_a_difundir, relacion_difusiones=usuario_que_pulsa_difundir)
    elimina_Difundir.relacion_difusiones.remove(usuario_que_pulsa_difundir)
    elimina_Difundir.save()
    rumor_a_difundir.num_difusion -=1
    rumor_a_difundir.save()
    eliminame=Rumor.objects.filter(contenido=rumor_a_difundir.contenido, username=usuario_que_pulsa_difundir)
    eliminame.delete()
    return HttpResponseRedirect('/')

@login_required
def borrarRumor(request, rumor_id):
    usuario=UserProfile.objects.get(user=request.user)
    rumor=Rumor.objects.filter(username=usuario, rumor_id=rumor_id)
    rumor.delete()
    return HttpResponseRedirect('/')
