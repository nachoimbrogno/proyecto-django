from django.urls import path
#Le importo las vistaas de usuarios, en este caso la de la propia apliacion:
from usuarios import views
#Importo el logoutview para poder usar la CBV.
from django.contrib.auth.views import LogoutView


#app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    #Directamente le paso el template en urls.py para que no vaya a las views.
    path('logout/', LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    path('cambio-contrasenia/', views.CambioContrasenia.as_view(), name='cambio_contrasenia'),
]
