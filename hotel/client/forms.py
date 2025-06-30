from django import forms
from .models import Client

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from django import forms
from .models import Client

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = Client
        fields = ['name', 'prenom', 'phone', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
from django import forms

from django import forms

class ReservationForm(forms.Form):
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date de début")
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date de fin")

class PaiementForm(forms.Form):
    montant = forms.FloatField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}))
    mode_paiement = forms.ChoiceField(choices=[('carte', 'Carte bancaire'), ('paypal', 'PayPal')])
from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16, min_length=16, 
        label="Numéro de carte",
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'})
    )
    card_expiry = forms.DateField(
        label="Date d'expiration",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    cvv = forms.CharField(
        max_length=3, min_length=3, 
        label="CVV",
        widget=forms.PasswordInput(attrs={'placeholder': '123'})
    )

from django import forms
from .models import Client

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'prenom', 'phone', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

from django import forms
from .models import Reclamation

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['chambre', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez votre problème ici...'})
        }
