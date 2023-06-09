from django import forms

class CreacionAnimalFormulario(forms.Form):
    nombre = forms.CharField(max_length=20)
    edad = forms.IntegerField()
    cant_dientes = forms.IntegerField(required=False)

#Formulario destinado a modificar datos en la base de datos
class ModificarAnimalFormulario(forms.Form):
    nombre = forms.CharField(max_length=20)
    edad = forms.IntegerField()
    cant_dientes = forms.IntegerField(required=False)

class BuscarAnimal(forms.Form):
    #Solo buscara por nombre , el required = False me permite que no complete nada en el campo al moento de buscar.
    nombre = forms.CharField(max_length=20, required=False)
