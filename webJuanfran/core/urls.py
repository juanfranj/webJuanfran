
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,  name = 'home'),
    path('registro/', views.register, name = 'registro'),
    path('registroAutomatico/', views.automaticRegister, name = 'registroAutomatico'),
    path('start/', views.start, name = 'start'),
    path('stop/', views.stop, name = 'stop'),
    path('registroManual/', views.registroManual, name = 'registroManual'),
    
]