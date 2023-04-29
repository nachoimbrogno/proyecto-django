from django.urls import path
#Le importo las vistaas de usuarios, en este caso la de la propia apliacion:
from usuarios import views
#Importo el logoutview para poder usar la CBV.
from django.contrib.auth.views import LogoutView


#app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    #Directamente le paso el template en urls.py para que no vaya a las views.
    path('logout/', LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
]
