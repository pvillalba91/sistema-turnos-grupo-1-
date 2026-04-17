from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_paciente, name='home_paciente'),
    path('home-profesional/', views.home_profesional, name='home_profesional'),
    path('home-recepcionista/', views.home_recepcionista, name='home_recepcionista'),
    path('home-admin/', views.home_admin, name='home_admin'),
]