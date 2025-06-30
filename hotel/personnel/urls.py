from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('',views.home,name='home'),
   path('/login',views.login_personnel,name='login_personnel'),
   # path('/dashboard',views.personnel_dashboard,name='personnel_dashboard'),
   path('/liste_client',views.liste_client,name='liste_client'),
   path('/ajouter/', views.ajouter_client, name='ajouter_client'),
   path('/modifier/<int:client_id>/', views.modifier_client, name='modifier_client'),
   path('/supprimer/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
   path('/liste_chambre',views.liste_chambre,name='liste_chambre'),
   path('/ajouter_chambre/', views.ajouter_chambre, name='ajouter_chambre'),
   path('/modifier_chambre/<int:chambre_id>/', views.modifier_chambre, name='modifier_chambre'),
   path('/supprimer_chambre/<int:chambre_id>/', views.supprimer_chambre, name='supprimer_chambre'),
   path('facture/pdf/<int:paiement_id>/', views.generer_facture_pdf, name='generer_facture_pdf'),
   path('/reservations/', views.liste_reservations, name='liste_reservations'),
   path('/reservation/preparer/', views.preparer_reservation, name='preparer_reservation'),
   path('/reservation/paiement/', views.payer_reservation, name='payer_reservation'),
   path('/reservations/modifier/<int:reservation_id>/', views.modifier_reservation, name='modifier_reservation'), 
   path('/reservations/supprimer/<int:reservation_id>/', views.supprimer_reservation, name='supprimer_reservation'),
   path('/reclamations/', views.display_reclamtion, name='liste_reclamations'),
   path('/logout/', views.logout_personnel, name='logout_personnel'),


 


]