
# Create your views here.



from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Client
from django.contrib import messages
from django.http import HttpResponse

def login(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                client = Client.objects.get(email=email)
                if client.check_password(password):
                    request.session['client_id'] = client.id
                    messages.success(request, f"Bienvenue {client.prenom} !")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Client.DoesNotExist:
                messages.error(request, "Client introuvable.")

    return render(request, 'client/login.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Client
from django.contrib import messages

def register(request):
    form = RegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(form.cleaned_data['password'])
            client.save()
            messages.success(request, "Inscription réussie ! Connectez-vous maintenant.")
            return redirect('login')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")

    return render(request, 'client/register.html', {'form': form})

def reservation(request):
    return render(request,'client/reservation.html')
def paiement(request):
    return render(request,'client/paiement.html')  
from django.shortcuts import render, redirect
from .models import Client , Chambre

def client_dashboard(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('client_login')

    client = Client.objects.get(id=client_id)
    chambres = Chambre.objects.all()

    # Afficher les paiements
    # paiements = Paiement.objects.filter(client=client)

    return render(request, 'client/dashboard.html', {
        'client': client,
        'chambres': chambres,
        # 'paiements': paiements,
    })

def client_logout(request):
    request.session.flush()  # Efface toutes les données de session
    return redirect('home')
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Chambre, Reservation, Paiement
from .forms import ReservationForm, PaymentForm
from django.contrib import messages
from datetime import datetime

def reserver_chambre(request, chambre_id):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('login')
    
    chambre = get_object_or_404(Chambre, id=chambre_id)
    client = get_object_or_404(Client, id=client_id)
    form = ReservationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        date_debut = form.cleaned_data['date_debut']
        date_fin = form.cleaned_data['date_fin']
        
        # Vérifier si la chambre est déjà réservée durant la période souhaitée
        conflits = Reservation.objects.filter(
            chambre=chambre,
            date_debut__lte=date_fin,
            date_fin__gte=date_debut
        )
        if conflits.exists():
            messages.error(request, "Cette chambre est déjà réservée pendant cette période.")
        else:
            # Calcul du nombre de nuits et du prix total
            try:
                nb_nuits = (date_fin - date_debut).days
                prix_total = float(chambre.prix) * nb_nuits
            except Exception as e:
                messages.error(request, "Erreur lors du calcul du prix total.")
                return render(request, 'client/reserver_chambre.html', {'form': form, 'chambre': chambre})
            
            # Stocker les informations de réservation dans la session pour les utiliser lors du paiement
            request.session['reservation_data'] = {
                'chambre_id': chambre.id,
                'date_debut': date_debut.strftime('%Y-%m-%d'),
                'date_fin': date_fin.strftime('%Y-%m-%d'),
                'prix_total': prix_total
            }
            # Redirige vers la page de paiement
            return redirect('payer_chambre')
    
    return render(request, 'client/reserver_chambre.html', {'form': form, 'chambres': chambre})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Chambre, Reservation, Paiement
from .forms import PaymentForm

def payer_chambre(request):
    reservation_data = request.session.get('reservation_data')
    client_id = request.session.get('client_id')

    if not reservation_data or not client_id:
        messages.error(request, "Aucune réservation en attente ou utilisateur non connecté.")
        return redirect('dashboard')

    chambre = get_object_or_404(Chambre, id=reservation_data['chambre_id'])
    client = get_object_or_404(Client, id=client_id)

    form = PaymentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Simuler un traitement de paiement (dans un vrai cas, intégrer Stripe/PayPal...)
        # Ici, on suppose que le paiement réussit toujours
        
        # Enregistrer le paiement
        Paiement.objects.create(
            client=client,
            montant=str(reservation_data['prix_total']),
            statut='Payé'
        )

        # Enregistrer la réservation
        Reservation.objects.create(
            client=client,
            chambre=chambre,
            date_debut=reservation_data['date_debut'],
            date_fin=reservation_data['date_fin'],
            prix_total=str(reservation_data['prix_total'])
        )

        # Nettoyer la session
        del request.session['reservation_data']

        messages.success(request, "Paiement effectué et réservation confirmée !")
        return redirect('dashboard')

    return render(request, 'client/paiement.html', {
        'form': form,
        'chambre': chambre,
        'reservation_data': reservation_data,
         'montant':str(reservation_data['prix_total'])
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ClientUpdateForm
from .models import Client

from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ClientUpdateForm
from .models import Client

def home(request):
    return render(request,'client/home.html')   
def modifier_infos_client(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('login')

    client = get_object_or_404(Client, id=client_id)

    # On garde l'ancien mot de passe au cas où il n'est pas modifié
    ancien_password = client.password

    form = ClientUpdateForm(request.POST or None, instance=client)

    if request.method == 'POST' and form.is_valid():
        updated_client = form.save(commit=False)
        nouveau_password = form.cleaned_data['password']

        # Si le mot de passe est différent, on le hache
        if nouveau_password != ancien_password:
            updated_client.password = make_password(nouveau_password)
        else:
            updated_client.password = ancien_password  # Inchangé

        updated_client.save()
        messages.success(request, "Vos informations ont été mises à jour avec succès.")
        return redirect('dashboard')

    return render(request, 'client/modifier_infos.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReclamationForm
from .models import Client, Reclamation

def soumettre_reclamation(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('client_login')

    client = get_object_or_404(Client, id=client_id)

    form = ReclamationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reclamation = form.save(commit=False)
        reclamation.client = client
        reclamation.save()
        messages.success(request, "Votre réclamation a été soumise avec succès.")
        return redirect('dashboard')

    return render(request, 'client/reclamation.html', {'form': form})


