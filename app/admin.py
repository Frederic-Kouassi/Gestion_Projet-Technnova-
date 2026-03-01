from django.contrib import admin

# Register your models here.
from .models import  Idee, Projet, Commentaire, Like, PartnershipRequest


admin.site.register(Idee)
admin.site.register(Projet)
admin.site.register(Commentaire)
admin.site.register(Like)
admin.site.register(PartnershipRequest)