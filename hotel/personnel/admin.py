from django.contrib import admin
from .models import Personnel
from client.models import Client, Chambre, Paiement, Reservation
# Register your models here.
admin.site.register(Personnel)
admin.site.register(Client)
admin.site.register(Chambre)
admin.site.register(Paiement)
admin.site.register(Reservation)
