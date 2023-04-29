from django.http import HttpResponse
#Para poder pasar la fecha en la funcion de mostrar_fecha
from datetime import datetime
#Iporto para poder laburar con template (en la vista de mi _primer_template)
from django.template import Template, Context, loader
#Me traigo la vista Animal de models.
from inicio.models import Animal
#Importo para laburar en render y el redirect en los formularios
from django.shortcuts import render, redirect
#metraigo el formulario de forms.py
from inicio.forms import CreacionAnimalFormulario, BuscarAnimal, ModificarAnimalFormulario
#Import para poder listar objetos con CBV
from django.views.generic.list import ListView
#Import para poder crear y modificar y eliminar objetos con CBV
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#Import para poder ver objetos con CBV
from django.views.generic.detail import DetailView
#Iporto para poder usar mixin 
from django.contrib.auth.mixins import LoginRequiredMixin
#Iporto para poder usar decoradores
from django.contrib.auth.decorators import login_required


def mi_vista(request):
    # return HttpResponse ("<h1>Mi primera vista</h1>")
    return render(request,'inicio/index.html',)

#VERSION CON HttpResponse
#Para devolver una fecha que guardo en dt con la funcion datime y formateo para que la muestre de una forma particular.
#ESTA COMENTADO PORQUE EN LA OTRA FUNCION DE MOSTRAR_FECHA LO USO PARA PASARLE VARIABLES A UN TEMPLATE.
# def mostrar_fecha(request):
#     dt = datetime.now()
#     dt_formateado = dt.strftime("%A %d %B %Y %I:%M")
#     return HttpResponse (f"<p>{dt_formateado}</p>")

def saludar(request,nombre,apellido):
    return HttpResponse(f"<h1>Hola {nombre} {apellido}</h1>")

def mi_primer_template(request):
    #Abro el archivo de template
    archivo = open(r'D:\nacho\Desktop\proyectos\proyecto-django\templates\mi_primer_template.html','r')
    #transformo el archivo en un template
    template = Template(archivo.read())
    #cierro el archivo
    archivo.close()
    contexto = Context()
    #Renderizo el template, seria como que se arme.
    template_renderizado = template.render(contexto)
    return HttpResponse(template_renderizado)

#Version con template.
def mostrar_fecha(request):
    dt = datetime.now()
    dt_formateado = dt.strftime("%A %d %B %Y %I:%M")
    #Abro el archivo de template (lo abro con loader porque odifiqué el path de donde leo los templates y ya, no es
    # un archivo de python sino que utilizo el loader)
    template = loader.get_template(r'inicio/mostrar_fecha.html')
    template_renderizado = template.render({'fecha': dt_formateado})
    return HttpResponse(template_renderizado)

def prueba_template(request):
    datos = {
        'nombre': 'Pepito',
        'apellido': 'Grillo',
        'edad':16,
        'años': [1995, 2004, 2017, 2021, 2022]
    }
    template = loader.get_template(r'inicio/prueba_template.html')
    template_renderizado = template.render(datos)
    return HttpResponse(template_renderizado)

@login_required
def prueba_render(request):
    datos = {'nombre': 'Pepe'}
    # template = loader.get_template(r'prueba_render.html')
    # template_renderizado = template.render(datos)
    # return HttpResponse(template_renderizado) 
    return render(request, r'inicio/prueba_render.html', datos)


#VISTAS COMUNES PARA ANIMALES

#V1
# def crear_animal(request):
#     animal = Animal(nombre='Ricardtio', edad= 3)
#     print (animal.nombre)
#     print(animal.edad)
#     animal.save()
#     datos = {'animal': animal }
#     template = loader.get_template(r'inicio/crear_animal.html')
#     template_renderizado = template.render(datos)
#     return HttpResponse(template_renderizado)

#V2 Con formulario manual y noel de django
# def crear_animal(request):
#     #Guardo en animal el objeto creado en models Animal, con request.POST lo que le digo es del post que viene
#     #toma el nombre. Lo mismo para edad. Luego en save lo guardo.
#     if request.method == 'POST':
#         animal = Animal(nombre= request.POST ['nombre'], edad= request.POST ['edad'])
#         animal.save()
#     return render(request, 'inicio/crear_animal_v2.html')

#V3 Con formulario de django
def crear_animal(request):
    if request.method == 'POST':
        #Creo un formulario del tipo CreacionAimalFormulario con la info que trae el post.
        formulario = CreacionAnimalFormulario(request.POST)
        #Verifico si el formulario es valido con la info que se nos pasa
        if formulario.is_valid():
            #Ahora le digo que los datos los tome desde
            datos_correctos = formulario.cleaned_data
            animal = Animal(nombre= datos_correctos ['nombre'], edad= datos_correctos ['edad'])
            animal.save()
            #Ahora para que vaya al formulario le digo que vaya al lista_formulario para eso cargo redirect en donde
            #exporto los paquetes. listar_aniamles es lo que le defini en name desde urls.py:
            return redirect('listar_animales')
    #en caso que no sea post o no sea valido vendrá aca:
    formulario = CreacionAnimalFormulario()
    return render(request, 'inicio/crear_animal_v3.html', {'formulario': formulario})
    


#Vista para mostrar los animales creados en crear animal
def lista_animales(request):
    #el request.GET es como un diccionario y puedo obtenet la informacion que esta en una llave y sino none
    nombre_a_buscar = request.GET.get('nombre', None)
    #Ahora sí, nombre a buscar no esta vacio que devuelva todo, pero si mandan otro filtro los que tiene 
    #nombre a buscar
    if nombre_a_buscar:
        #Busco los animales que yo pongo en nombre a buscar con el get. Lo que hace icontains es buscar los 
        #que contienen lo que yo quiero buscar y no lo exacto
        animales = Animal.objects.filter(nombre__icontains=nombre_a_buscar)
    else:
        animales = Animal.objects.all()
    formulario_busqueda = BuscarAnimal()
    return render(request, 'inicio/lista_animales.html', {'animales': animales, 'formulario': formulario_busqueda})

#Funcion para borrar animales de la base, el id_animales lo tomara el post de la url que le dara el id del animal.
def eliminar_animal(request,id_animal):
    #utilizó el Animal.objects.get ya que el get nos va a traer informacion. Indicandole por atributo, en este caso el id
    animal_a_eliminar = Animal.objects.get(id=id_animal)
    #borro el objeto, el animal en este caso.
    animal_a_eliminar.delete()
    #Esto lo hago para que luego de eliminar vuelva a la  lista de animales.
    return redirect('listar_animales')

#Funcion para mostrar un animal especifico de la base, el id_animales lo tomara el post de la url que le dara el id del animal.
def mostrar_animal(request,id_animal):
    #utilizó el Animal.objects.get para buscar el animal especifico (el get nos va a traer informacion). Indicandole por atributo, en este caso el id
    animal_a_mostrar = Animal.objects.get(id=id_animal)
    #Hago un nuevo render para mostrarlo, que pasa el request y el html es mostrar animal y al contexto le voy
    #a estar pasando el animal a mostrar
    return render(request, 'inicio/mostrar_animal.html', {'animal_a_mostrar': animal_a_mostrar})

#Vista para modificar animal en la base:
def modificar_animal(request, id_animal):
    animal_a_modificar = Animal.objects.get(id=id_animal)
    #Valido si el request viene por POST
    if request.method == "POST":
        #guarda el formulario para modificar y guardo en la request del POST
        formulario = ModificarAnimalFormulario(request.POST)
        if formulario.is_valid():
            data_limpia = formulario.cleaned_data
            #Ya tengo que vine por post, arme el formulario con la info del request y valide que es valido el
            #formulario. Guardo la data en data limpia y actualizo los datos.
            #a la variable creada al ppio de la funcion le actualizo el nombre y la edad.
            animal_a_modificar.nombre = data_limpia['nombre']
            animal_a_modificar.edad = data_limpia['edad']
            animal_a_modificar.save()
            return redirect('listar_animales')
    #Si no viene por post le paso el formulario vacio, el initial es para que al momento de ver el campo por pantalle
    #te muestre el valor que tiene actualmente.
    formulario = ModificarAnimalFormulario(initial={"nombre": animal_a_modificar.nombre, "edad": animal_a_modificar.edad})
    #Retorno un render con el request y un template que es el template donde este el formulario para modificar datos.
    #le pasamos donde estara el html y el contexto es el formulario y el id del animal. Recordar crear el html en 
    # teplates
    return render(request, 'inicio/modificar_animales.html', {'formulario': formulario, 'id_animal': id_animal})



#CBV (CLASES BASADAS EN VISTAS) VISTAS PARA ANIMALES
#a la clase se le tiene que pasar como argumento ListView
class ListaAnimales(ListView):
    #primero le tengo que decir el modelo con el que va a trabajar.
    model = Animal
    #Despues el template con el que va a laburar. Ya no le paso el diccionario sino que recibira el un object_list.
    #generado automaticamente por django
    template_name = 'inicio/CBV/lista_animales.html'

#a la clase se le tiene que pasar como argumento CreatedView 
class CrearAnimal(CreateView):
    #primero le tengo que decir el modelo con el que va a trabajar.
    model = Animal
    #Despues el template con el que va a laburar. Ya no le paso el diccionario sino que recibira el un form.
    #generado automaticamente por django
    template_name = 'inicio/CBV/crear_animal_v3.html'
    #PAra que cuando se cree el objeto correctamente con la vista un animal quiero que vaya a esa url, para eso se le pasa 
    # la url base a la que quiero que vaya (el contexto), desde el puerto para atras: 
    #la url es http://127.0.0.1:8000/inicio/animales/  --> inicio/animales/ 
    success_url = '/inicio/animales/'
    # aca se le indica los capos que quiero que se le pida al usuario en la creacion:
    fields = ['nombre', 'edad']

#a la clase se le tiene que pasar como argumento UpdateView. Para editar es igual que crear
class ModificarAnimal(LoginRequiredMixin, UpdateView):
    #primero le tengo que decir el modelo con el que va a trabajar.
    model = Animal
    #Despues el template con el que va a laburar. Ya no le paso el diccionario sino que recibira el un form.
    #generado automaticamente por django
    template_name = 'inicio/CBV/modificar_animales.html'
    #PAra que cuando se cree el objeto correctamente con la vista un animal quiero que vaya a esa url, para eso se le pasa 
    # la url base a la que quiero que vaya (el contexto), desde el puerto para atras: 
    #la url es http://127.0.0.1:8000/inicio/animales/  --> inicio/animales/ 
    success_url = '/inicio/animales/'
    # aca se le indica los capos que quiero que se le pida al usuario en la creacion:
    fields = ['nombre', 'edad', 'cant_dientes']

#a la clase se le tiene que pasar como argumento DeleteView 
class EliminarAnimal(LoginRequiredMixin, DeleteView):
    #primero le tengo que decir el modelo con el que va a trabajar.
    model = Animal
    #Despues el template con el que va a laburar. Ya no le paso el diccionario sino que recibira el un form.
    #generado automaticamente por django
    template_name = 'inicio/CBV/eliminar_animal.html'
    #PAra que cuando se cree el objeto correctamente con la vista un animal quiero que vaya a esa url, para eso se le pasa 
    # la url base a la que quiero que vaya (el contexto), desde el puerto para atras: 
    #la url es http://127.0.0.1:8000/inicio/animales/  --> inicio/animales/ 
    success_url = '/inicio/animales/'

#a la clase se le tiene que pasar como argumento DetailView 
class MostrarAnimal(DetailView):
    #primero le tengo que decir el modelo con el que va a trabajar.
    model = Animal
    #Despues el template con el que va a laburar. Ya no le paso el diccionario sino que recibira el un form.
    #generado automaticamente por django
    template_name = 'inicio/CBV/mostrar_animal.html'
    #PAra que cuando se cree el objeto correctamente con la vista un animal quiero que vaya a esa url, para eso se le pasa 
    # la url base a la que quiero que vaya (el contexto), desde el puerto para atras: 
    #la url es http://127.0.0.1:8000/inicio/animales/  --> inicio/animales/ 
    success_url = '/inicio/animales/'