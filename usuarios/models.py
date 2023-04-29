from django.db import models
#Me traigo el user porque 
from django.contrib.auth.models import User


# Create your models here.

class InformacionExtra(models.Model):
    #como el avatar será una imagen le tengo que decir que use el modelo de image field y le paso lo siguiente
    #identifica en que carpeta vamos a guardar las imagene - defino la carpeta avatares y no es necesario tener 
    #imagenes cargadas para eso uso el null y blanck)
    avatar = models.ImageField(upload_to='avatares', null=True, blank=True)
    #Me traigo el usuario que tendra una relacion con el user. Para eso utilizo la foreingkey que lo que me dice
    #es que contendra informacion sobre otro campo.
    #O sea tendra un campo relacionado por clave foranea a los modelos Users, entonces lo que guarda es el identificador
    # (el id en la base) de un objeto User, por eso asi sabre a que usuario estara relacionado
    #user = models.ForeignKey(User, on_delete=models.CASCADE), el on delete indica que cuando se borra el usuario
    #se borra toda la informacion extra asociada a él
    #No voy a usar foreingKey porque eso es para mucha informacion y como solo tendrá un avatar el usuario
    #no hace falta, entonces usaremos OneToOne y facilitará el acceso a la ingormacion extra del usuario.
    user = models.OneToOneField(User, on_delete=models.CASCADE)