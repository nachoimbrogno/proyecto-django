from django.http import HttpResponse
#Para poder pasar la fecha en la funcion de mostrar_fecha
from datetime import datetime
#Iporto para poder laburar con template (en la vista de mi _primer_template)
from django.template import Template, Context

def mi_vista(request):
    return HttpResponse ("<h1>Mi primera vista</h1>")

#Para devolver una fecha que guardo en dt con la funcion datime y formateo para que la muestre de una forma particular.
def mostrar_fecha(request):
    dt = datetime.now()
    dt_formateado = dt.strftime("%A %d %B %Y %I:%M")
    return HttpResponse (f"<p>{dt_formateado}</p>")

def saludar(request,nombre,apellido):
    return HttpResponse(f"<h1>Hola {nombre} {apellido}</h1>")

def mi_primer_template(request):
    archivo = open(r'D:\nacho\Desktop\proyectos\proyecto-django\templates\mi_primer_template.html','r')
    template = Template(archivo.read())
    archivo.close()
    contexto = Context()
    template_renderizado = template.render(contexto)
    return HttpResponse(template_renderizado)

