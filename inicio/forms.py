from django import forms

class CreacionAnimalFormulario(forms.Form):
    nombre = forms.CharField(max_length=20)
    edad = forms.IntegerField()