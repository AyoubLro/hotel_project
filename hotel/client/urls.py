from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('/login',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.client_logout,name='logout'),
    path('dashboard/',views.client_dashboard,name='dashboard'),
    path('reserver/<int:chambre_id>/', views.reserver_chambre, name='reserver_chambre'),
    path('payer/', views.payer_chambre, name='payer_chambre'),
    path('modifier-infos/', views.modifier_infos_client, name='modifier_infos'),
    path('reclamation/', views.soumettre_reclamation, name='soumettre_reclamation'),

   

]