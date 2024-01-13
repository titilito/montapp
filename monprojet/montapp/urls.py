from django.urls import path
from django.urls import reverse
from .views import login_view, accueil_view, logout_view, reset_password_view, password_reset_request, planning_url_view, documents_url_view, factures_url_view, get_evenements, create_evenement, statistiques_utilisateur, DocumentListView, document_upload, infos, upload_facture, liste_factures, lister_factures, account_info

urlpatterns = [
    path('', accueil_view, name='accueil'),
    path('get-evenements/', get_evenements, name='get_evenements'),
    path('accueil/', accueil_view, name='accueil'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-password/', reset_password_view, name='reset_password'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('planning-url/', planning_url_view, name='planning_url'),
    path('upload/', documents_url_view, name='documents_url'),
    path('factures-url/', factures_url_view, name='factures_url'),
    path('create-evenement/', create_evenement, name='create_evenement'),
    path('statistiques-utilisateur/', statistiques_utilisateur, name='statistiques_utilisateur'),
    path('upload/', document_upload, name='document_upload'),
    path('list/', DocumentListView.as_view(), name='document_list'),
    path('infos-url/', infos, name='infos_url'),
    path('upload_facture/', upload_facture, name='upload_facture'),
    path('factures/', liste_factures, name='liste_factures'),
    path('lister_factures/', lister_factures, name='lister_factures'),
    path('account_info/', account_info, name='account_info'),
]
