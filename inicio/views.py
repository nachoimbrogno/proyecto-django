from django.http import HttpResponse
#Para poder pasar la fecha en la funcion de mostrar_fecha
from datetime import datetime
#Iporto para poder laburar con template (en la vista de mi _primer_template)
from django.template import Template, Context, loader
#Me traigo la vista Animal de models.
from inicio.models import Animal
#Importo para laburar en render
from django.shortcuts import render

def mi_vista(request):
    return HttpResponse ("<h1>Mi primera vista</h1>")

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

def crear_animal(request):
    animal = Animal(nombre='Ricardtio', edad= 3)
    print (animal.nombre)
    print(animal.edad)
    animal.save()
    datos = {'animal': animal }
    template = loader.get_template(r'inicio/crear_animal.html')
    template_renderizado = template.render(datos)
    return HttpResponse(template_renderizado)

def prueba_render(request):
    datos = {'nombre': 'Pepe'}
    # template = loader.get_template(r'prueba_render.html')
    # template_renderizado = template.render(datos)
    # return HttpResponse(template_renderizado) 
    return render(request, r'inicio/prueba_render.html', datos)