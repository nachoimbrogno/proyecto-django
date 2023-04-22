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
from inicio.forms import CreacionAnimalFormulario, BuscarAnimal

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

def prueba_render(request):
    datos = {'nombre': 'Pepe'}
    # template = loader.get_template(r'prueba_render.html')
    # template_renderizado = template.render(datos)
    # return HttpResponse(template_renderizado) 
    return render(request, r'inicio/prueba_render.html', datos)

