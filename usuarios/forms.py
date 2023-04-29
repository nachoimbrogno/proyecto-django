from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#creo un formulario "MiFormularioDeCreacion" y le pasó coo basico el UserCreationForm, antes importarlo
class MiFormularioDeCreacion(UserCreationForm):
    #Primero le digo los capos que quiero que remplace del padre:
    #Agrego el campo mail
    email = forms.EmailField()
    #Modifico para que no diga password al momento de  perdi password y confirmacion sino contraseña, mediante un 
    #label. el widget=forms.PasswordInput es para enmascarar la pwd al escribirla en la url.
    password1 = forms.CharField(label = 'Contrasenia', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Repetir Contrasenia',widget=forms.PasswordInput)
    #No quiero que muestre las leyendas que figuran al cargar las pwds. Para eso usamos class Meta, esto contiene
    #la informacion que va a hilar por atras el formulario, primero le paso el modelo que va a trabajar, User en
    #este caso: antes importar: from django.contrib.auth.models import User
    class Meta:
        model = User
        #Le indico que campos quiere que muestre
        fields = ['username', 'email', 'password1', 'password2']
        #Para tapar el texto de ayuda al momento de loguearse:
        #lo que e le dice es que por cada clave k  del diccionario genere un string vacio.
        help_texts = {k: '' for k in fields}

    