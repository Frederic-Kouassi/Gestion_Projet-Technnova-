from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.

class Projet(models.Model):
    name = models.CharField(max_length=128, default="Nom par défaut")
    responsable = models.CharField(max_length=128, default="Responsable par défaut")
    objectif = models.CharField(max_length=128, default="Objectif par défaut")

    membres = models.TextField(blank=True)
    description = models.TextField(blank=True)

    date_debut = models.DateField(default=datetime.today, blank=True, null=True)
   
    def __str__(self):
        return self.name

   
    

class Idee(models.Model):
    name= models.CharField(max_length=128)
    description= models.TextField(blank=True)
    categorie= models.CharField(max_length=128)
    date=models.DateTimeField(default=datetime.now, blank=True)
    
    
    def __str__(self):
        return self.name
    
    
class Commentaire(models.Model):
    projet = models.ForeignKey(Idee, on_delete=models.CASCADE, related_name="commentaires")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    projet = models.ForeignKey(Idee, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('projet', 'user')  # un seul like par utilisateur
    

class PartnershipRequest(models.Model):
    DOMAINE_CHOICES = [
        ('Technologie', 'Technologie'),
        ('Finance', 'Finance'),
        ('Santé', 'Santé'),
        ('Éducation', 'Éducation'),
        ('Autre', 'Autre'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Nom de l'organisation")
    domaine = models.CharField(max_length=50, choices=DOMAINE_CHOICES, verbose_name="Domaine d'activité")
    email = models.EmailField(verbose_name="Email de contact")
    message = models.TextField(verbose_name="Message")
    image = models.ImageField(upload_to='partnership_images/', null=True, blank=True, verbose_name="Logo ou image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.domaine}" 


    
    
    
# Pour les projets associés






    


    