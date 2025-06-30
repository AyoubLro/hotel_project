from django import forms

class PersonnelLoginForm(forms.Form):
    email = forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
from django import forms
from client.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'prenom', 'phone', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
from django import forms
from client.models import Chambre

class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = ['numero', 'prix', 'type', 'etat', 'image']
from django import forms
from client.models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client', 'chambre', 'date_debut', 'date_fin', 'prix_total']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }
