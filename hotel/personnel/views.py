from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'client/home.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Personnel
from .forms import PersonnelLoginForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Personnel
from .forms import PersonnelLoginForm
from client.models import Client
from client.models import Chambre

def login_personnel(request):
    form = PersonnelLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        mot_de_passe = form.cleaned_data['mot_de_passe']

        try:
            personnel = Personnel.objects.get(email=email)
            if mot_de_passe == personnel.password:  # Vérification en clair
                request.session['personnel_id'] = personnel.id
                return redirect('liste_client')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except Personnel.DoesNotExist:
            messages.error(request, "Email introuvable.")

    return render(request, 'personnel/login_personnel.html', {'form': form})

# def personnel_dashboard(request):
#     personnel_id = request.session.get('personnel_id')
#     if not personnel_id:
#         return redirect('login_personnel')

    # return render(request, 'personnel/personnel_dashboard.html')
def liste_client(request):
    personnel_id = request.session.get('personnel_id')
    if not personnel_id:
        return redirect('login_personnel')

    query_nom = request.GET.get('nom', '')
    query_prenom = request.GET.get('prenom', '')

    clients = Client.objects.all()

    if query_nom:
        clients = clients.filter(name__icontains=query_nom)
    if query_prenom:
        clients = clients.filter(prenom__icontains=query_prenom)

    context = {
        'clients': clients,
        'query_nom': query_nom,
        'query_prenom': query_prenom
    }
    return render(request, 'personnel/liste_client.html', context)


from django.shortcuts import render, redirect
from .forms import ClientForm

def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_client')
    else:
        form = ClientForm()
    return render(request, 'personnel/ajouter_client.html', {'form': form})

from django.shortcuts import get_object_or_404

def modifier_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('liste_client')
    return render(request, 'personnel/modifier_client.html', {'form': form, 'client': client})

def supprimer_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_client')
    return render(request, 'personnel/confirmer_suppression.html', {'client': client})
from .forms import ChambreForm
def liste_chambre(request):
    chambres=Chambre.objects.all()
    return render(request, 'personnel/liste_chambre.html', {'chambres': chambres})
def ajouter_chambre(request):
    if request.method == 'POST':
        form = ChambreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_chambre')
    else:
        form = ChambreForm()
    return render(request, 'personnel/ajouter_chambre.html', {'form': form})
from django.shortcuts import get_object_or_404

def modifier_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    form = ChambreForm(request.POST or None, request.FILES or None, instance=chambre)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('liste_chambre')
    return render(request, 'personnel/modifier_chambre.html', {'form': form, 'chambre': chambre})
def supprimer_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == 'POST':
        chambre.delete()
        return redirect('liste_chambre')
    return render(request, 'personnel/confirmer_suppression_chambre.html', {'chambre': chambre})

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from client.models import Paiement
import io

def generer_facture_pdf(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    template_path = 'personnel/facture_pdf.html'
    context = {'paiement': paiement}

    # Charger le template
    template = get_template(template_path)
    html = template.render(context)

    # Créer un buffer mémoire
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{paiement.id}.pdf"'

    # Générer le PDF
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

from client.models import Reservation
from .forms import ReservationForm
def liste_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'personnel/liste.html', {'reservations': reservations})
def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_reservations')
    else:
        form = ReservationForm()
    return render(request, 'personnel/ajouter.html', {'form': form})
from django.shortcuts import get_object_or_404

def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('liste_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'personnel/modifier.html', {'form': form})
def supprimer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('liste_reservations')
    return render(request, 'personnel/supprimer.html', {'reservation': reservation})

from .forms import ReservationForm
from client.models import Paiement

from django.shortcuts import render, redirect
from .forms import ReservationForm

def preparer_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Stocker uniquement des données sérialisables
            request.session['reservation_data'] = {
                'client': data['client'].id,
                'chambre': data['chambre'].id,
                'date_debut': str(data['date_debut']),
                'date_fin': str(data['date_fin']),
                'prix_total': data['prix_total'],
            }
            return redirect('payer_reservation')
    else:
        form = ReservationForm()
    
    return render(request, 'personnel/preparer.html', {'form': form})


from client.models import Client, Chambre, Paiement, Reservation
from django.shortcuts import get_object_or_404

def payer_reservation(request):
    data = request.session.get('reservation_data')
    if not data:
        return redirect('preparer_reservation')
    
    client = get_object_or_404(Client, id=data['client'])
    chambre = get_object_or_404(Chambre, id=data['chambre'])

    if request.method == 'POST':
        # Créer le paiement
        Paiement.objects.create(
            client=client,
            # chambre=chambre,
            montant=data['prix_total']
        )
        # Créer la réservation
        Reservation.objects.create(
            client=client,
            chambre=chambre,
            date_debut=data['date_debut'],
            date_fin=data['date_fin'],
            prix_total=data['prix_total']
        )
        # Nettoyer la session
        del request.session['reservation_data']
        return redirect('liste_reservations')

    return render(request, 'personnel/paiement.html', {
        'client': client,
        'chambre': chambre,
        'prix': data['prix_total']
    })
from client.models import Reclamation
def display_reclamtion(request):
    reclamation=Reclamation.objects.all()
    return render(request, 'personnel/reclamation.html', {'reclamation': reclamation})
def logout_personnel(request):
    request.session.flush()  # Efface toutes les données de session
    return redirect('home')