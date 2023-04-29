from django.shortcuts import render, redirect
#para poder usuar el autenticador de Django
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
#Para poder usuar el authenticate de Django
from django.contrib.auth import authenticate, login as django_login
from usuarios.forms import MiFormularioDeCreacion


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
