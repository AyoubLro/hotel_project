from django.db import models

# Create your models here.
class Personnel(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
     return f"{self.name} {self.prenom}"