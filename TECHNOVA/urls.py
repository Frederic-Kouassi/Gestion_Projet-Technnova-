from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views import index,profile_utilisateurs, addemail,addpassword, profil, idee, sign_in,detail_projet,supprimer_projet, logout_user,liker_projet,commenter_projet, sign_up,partenariats,document, liste_projets

urlpatterns = [
    path('',index, name='index'),
    path('profil/',profil, name='profil'),
    path('logout_user/',logout_user, name='logout_user'),
    path('idee/',idee, name='idee'),
    path('sign_in/',sign_in, name='sign_in'),
    path('sign_up/',sign_up, name='sign_up'),
    path('addemail/',addemail, name='addemail'),
    path('addpassword/<str:email>/',addpassword, name='addpassword'),
     path('profile_utilisateurs/',profile_utilisateurs, name='profile_utilisateurs'),
    
    # urls.py
    path('projet/<int:projet_id>/',detail_projet, name='detail_projet'),


    # ...
    path('projet/<int:projet_id>/supprimer/',supprimer_projet, name='supprimer_projet'),




    path('partenariats/',partenariats, name='partenariats'),
   
    path('documents/',document, name='document'),
    path('liste_projets/',liste_projets, name='liste_projets'),
    path('commenter/<int:projet_id>/', commenter_projet, name='commenter_projet'),

    # ❤️ Like
    path('liker/<int:projet_id>/', liker_projet, name='liker_projet'),

    path('admin/', admin.site.urls),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
