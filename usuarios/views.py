from django.shortcuts import render, redirect
#para poder usuar el autenticador de Django
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
#Importo para poder usar la clase basada en vista para modificar la contraaseña
from django.contrib.auth.views import PasswordChangeView
#Para poder usuar el authenticate de Django
from django.contrib.auth import authenticate, login as django_login
from usuarios.forms import MiFormularioDeCreacion, EdicionDatosUsuario
#Iporto para poder usar decoradores
from django.contrib.auth.decorators import login_required
#Para poder en success_url poner un "alias" y no el string con el path a donde ir
from django.urls import reverse_lazy

# Create your views here.

#Vista para la autenticacion de usuarios
def login(request):
    #AuthenticationForm es un formulario por defecto de django para el login de usuarios
    #Valido si el request viene por POST
    if request.method == "POST":
        #Para el caso del AuthenticationForm cambia la forma de pasarle los datos al formulario.
        #1- primero le paso el request.
        #2- le paso data con el request post, osea los datos del post.
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            #Dentro del post que llega tomo el usuario, eso esta en el formulario que ya esta validado si llego aca
            nombre_usuario = formulario.cleaned_data.get('username')
            #Dentro del post que llega tomo la pwd, eso esta en el formulario que ya esta validado si llego aca
            contrasenia = formulario.cleaned_data.get('password')
            #guardo en usuario (con el methodo authenticate) los datos que obtuve del post en el forulario y que
            #guarde en nombre_usuario y password (para esto from django.contrib.auth import authenticate )
            usuario = authenticate(username=nombre_usuario, password=contrasenia)
            #una vez que tengo el usuario le digo que se loguee, para eso debo importar la funcion login de django.
            #from django.contrib.auth import authenticate, login as django_login (pongo el as django porque login
            # se llama la funcion esta y va a entrar en conflicto, entonces le pongo un alias)
            django_login(request, usuario)
            return redirect ('inicio')
        else:
            #si la informacion que viene no es valida ira a la misma pagina y le mostraré los errores en la vista.
            return render(request, 'usuarios/login.html',{'formulario':formulario})
    #si entra por get pedirá cargar el formulario para el login por eso lo paso vacio.
    formulario = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'formulario':formulario})

#Funcion para la creacion de un usuario
def registro(request):
    if request.method == "POST":
        #Trabajo con el formulario de creacion que cree en forms: MiFormularioDeCreacion
		#Este es el formulario de django para la creacion de usuarios
        #a formulario le asigno el formulario que cree en forms.
        formulario = MiFormularioDeCreacion(request.POST)
        if formulario.is_valid():
            #La particularidad del formulario permite guardarlo de una, solo este formulario no se hace claenes data
            formulario.save()
            #Si creo el usuario con exito lo derivo a la url de login para que pruebe
            return redirect ('login')
        else:
            return render(request, 'usuarios/registro.html',{'formulario':formulario})
    #formulario = UserCreationForm() --> lo comento para poder utilizar el formulario customizado
    #a formulario le asigno el formulario que cree en forms.
    formulario = MiFormularioDeCreacion()
    return render(request, 'usuarios/registro.html', {'formulario': formulario})

#Vista para editar daros del usuario. Necesito importar el formulario que cree en forms(from usuarios.forms import EdicionDatosUsuario )
#uso el login_required porque solo acceder cuando el usuario esta logueado para cambiar su perfil.
#recordar importar el decorador: from django.contrib.auth.decorators import login_required
@login_required
def editar_perfil(request):
    if request.method == "POST":
        #Este formulario trabaja distinto, le tengo que indicar cuál es el usuario que va a modificar para
        #luego poder guardarlo, para eso le agrego un nuevo argument instance que le voy a pasar el usuario
        #que esta logueado, eso lo tomo del request.
        formulario = EdicionDatosUsuario(request.POST, instance=request.user)
        if formulario.is_valid():
            formulario.save()
            return redirect ('inicio')
        else:
            return render(request, 'usuarios/editar_perfil.html',{'formulario':formulario})
    #le paso el instance para que genere el formulario con los datos del usuario que esta logueado. Aca irá
    #cuando el usuario esta logueada y le mostrará los datos personales gracias el request.user
    formulario = EdicionDatosUsuario(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'formulario': formulario})

#Clase basa en vista parra modificar la contraseña, por eso que herede PasswordChangeView
class CambioContrasenia(PasswordChangeView):
    #indicamos el template name, osea el template donde esta el html.
    template_name = 'usuarios/cambiar_contrasenia.html'
    #Recordar importar  para poder usar el reverse_lazy: from django.urls import reverse_lazy
    success_url = reverse_lazy('editar_perfil')
