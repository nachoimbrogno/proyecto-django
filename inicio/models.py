from django.db import models

# Create your models here.
class Animal(models.Model):
    nombre = models.CharField(max_length=20)
    edad = models.IntegerField()
    #Creo el str para darle formato al momento de mostrarlo por el admin.
    def __str__(self):
        return f'Soy {self.nombre}, tengo {self.edad}'


class Persona(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    
    #Creo el str para darle formato al momento de mostrarlo por el admin.
    def __str__(self):
        return f'Soy {self.nombre} {self.apellido}, nací en {self.fecha_nacimiento}'