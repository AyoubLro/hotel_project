from django.db import models
from django.contrib.auth.hashers import make_password, check_password
class Client(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return f"{self.prenom} {self.name}"

class Chambre(models.Model):
    TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
    ]

    numero = models.CharField(max_length=100)
    image = models.ImageField(upload_to='x',default='')
    prix = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    etat = models.CharField(max_length=100)
    def __str__(self):
        return f"Chambre {self.numero} ({self.type})"

class Paiement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    montant = models.FloatField(max_length=20,default=0)
    date_paiement = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    statut = models.CharField(max_length=20, choices=[('En attente', 'En attente'), ('Payé', 'Payé')], default='En attente')

    def __str__(self):
        return f"Paiement de {self.client.prenom} {self.client.name} pour {self.montant}€"


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date_debut = models.CharField(max_length=100)
    date_fin = models.CharField(max_length=100)
    prix_total = models.CharField(max_length=100)

class Reclamation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    description = models.TextField()