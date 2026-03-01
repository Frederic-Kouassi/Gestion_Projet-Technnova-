from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils.html import escape
from django.contrib import messages
from app.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404



def index(request):
    if request.method == "POST":
        type_objet = request.POST.get("type_objet")

        # Traitement d'une idée
        if type_objet == "idee":
            name = escape(request.POST.get("name"))
            description = escape(request.POST.get("description"))
            categorie = escape(request.POST.get("categorie"))
            date = request.POST.get("date_input")

            Idee.objects.create(
                name=name,
                description=description,
                categorie=categorie,
                date=date
            )

        # Traitement d'un projet
        elif type_objet == "projet":
            name = escape(request.POST.get("name"))
            responsable = escape(request.POST.get("responsable"))
            description = escape(request.POST.get("description"))
            objectif = escape(request.POST.get("objectif"))
            membres_list = request.POST.getlist("membres")  # Plusieurs valeurs
            membres = ", ".join([escape(m) for m in membres_list])
            date_debut = request.POST.get("date_debut")

            Projet.objects.create(
                name=name,
                responsable=responsable,
                description=description,
                objectif=objectif,
                membres=membres,
                date_debut=date_debut
            )

        return redirect("index")
    
   
    idees = Idee.objects.all()
    projets = Projet.objects.all()

    return render(request, 'app/dashbaord.html', {
        'idees': idees,
        'projets': projets
    })


def profil(request):
    return render(request, 'app/profile.html')


def idee (request):
    projets = Idee.objects.all().prefetch_related('commentaires', 'likes')
    return render(request, 'app/ideesinnovantes.html', {'projets': projets})

    

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username):
            messages.error(request, 'Ce nom  est déjà pris.')
            return redirect('sign_up')

        if User.objects.filter(email=email):
            messages.error(request, 'Cette adresse est déjà utilisée.')
            return redirect('sign_up')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("index")

    return render(request, 'app/sign-up.html')


def logout_user(request):
    logout(request)
    return redirect("sign_in")


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Identifiants invalides.")

    return render(request, 'app/sign-in.html')




def detail_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    return render(request, 'app/projet.html', {'projet': projet})



def partenariats(request):
    
    if request.method == "POST":
        name = request.POST.get("name")
        domaine = request.POST.get("domaine")
        email = request.POST.get("email")
        message = request.POST.get("message")
        image = request.FILES.get("image") 
        print(request.POST)
        
        request_obj = PartnershipRequest.objects.create(
            name=name,
            domaine=domaine,
            email=email,
            message=message,
            image=image
        )

        return redirect("partenariats")  
    
    partenaire =  PartnershipRequest.objects.all()
    return render(request, 'app/partenariats.html', context={"partenaire": partenaire})


def document(request):
    return render(request, 'app/documents.html')


def commenter_projet(request, projet_id):
    if request.method == 'POST':
        texte = request.POST.get('texte')
        projet = Idee.objects.get(id=projet_id)
        Commentaire.objects.create(projet=projet, auteur=request.user, texte=texte)
        return redirect('idee')


def liker_projet(request, projet_id):
    projet = Idee.objects.get(id=projet_id)
    like, created = Like.objects.get_or_create(projet=projet, user=request.user)
    if not created:
        like.delete() 
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': projet.likes.count()})

def liste_projets(request):
    
    projets = Idee.objects.all().prefetch_related('commentaire_set', 'likes')
    return render(request, 'app/ideesinnovantes.html', {'projets': projets})


def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)

    if request.method == "POST":
        projet.delete()
        messages.success(request, "Le projet a été supprimé avec succès.")
        return redirect('index')  # ou la vue vers laquelle tu veux revenir

    return render(request, 'app/projet.html', {'projet': projet})

#f fonction pour verification de l'eamil

def addemail(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect("addemail")  

        user = User.objects.filter(email=email).first() 

        if user:
            return redirect("addpassword", email=email)
        else:
            messages.error(
                request,
                "Cette adresse email ne correspond à aucun compte. Veuillez créer un compte."
            )
            return redirect("addemail")  

    return render(request, "app/addemail.html")

 
 
 # fonction pour changer le mot de passe apres verification
 
def addpassword(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('sign_in')

    if request.method == "POST":
        password = request.POST.get("password")
        password_confirm = request.POST.get("passwordconfirm")

        if not password or not password_confirm:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect("addpassword", email=email)

        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas. Veuillez réessayer.")
            return redirect("addpassword", email=email)

        if len(password) < 5:
            messages.error(request, "Le mot de passe est trop court (minimum 8 caractères).")
            return redirect("addpassword", email=email)

       
        user.set_password(password)
        user.save()  

        messages.success(request, "Votre mot de passe a bien été modifié. Connectez-vous maintenant.")
        return redirect('sign_in')

    context = {
        'email': email
    }

    return render(request, 'app/addpassword.html', context)



def profile_utilisateurs(request):
    
    return render(request, 'app/profile_utilisateurs.html')








