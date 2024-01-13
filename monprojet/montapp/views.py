# monprojet/montapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count, F, ExpressionWrapper, fields, Sum
import json
from django.views.decorators.http import require_POST
from django.db.models.functions import ExtractYear, Cast
from datetime import timedelta
from .models import Document, Evenement, Facture
from .forms import LoginForm, DocumentForm, FactureForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def account_info(request):
    user = request.user
    groups = user.groups.all()  # Obtenez les groupes auxquels l'utilisateur appartient
    permissions = {}
    
    # Obtenez les permissions dans chaque groupe
    for group in groups:
        permissions[group.name] = list(group.permissions.values_list('codename', flat=True))
    
    context = {
        'user': user,
        'permissions': permissions,
    }
    
    return render(request, 'montapp/account_infos.html', context)

def lister_factures(request):
    factures = Facture.objects.all()
    return render(request, 'montapp/liste_factures.html', {'factures': factures})

def liste_factures(request):
    dernières_factures = Facture.objects.all().order_by('-id')[:5]

    # Calcul de la répartition par utilisateur
    répartition_par_utilisateur = {}
    utilisateurs = User.objects.all()
    total_factures = Facture.objects.aggregate(total=Sum('montant'))['total'] or 0
    part_par_utilisateur = round(total_factures / utilisateurs.count(), 2)

    for utilisateur in utilisateurs:
        répartition_par_utilisateur[utilisateur.username] = part_par_utilisateur

    return render(request, 'montapp/factures.html', {
        'dernières_factures': dernières_factures,
        'répartition_par_utilisateur': répartition_par_utilisateur
    })

@login_required
def upload_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = form.cleaned_data['fichier']
            # Vérifier si le fichier est un PDF et sa taille est inférieure à 20 Mo
            if fichier.content_type != 'application/pdf' or fichier.size > 20 * 1024 * 1024:
                form.add_error('fichier', 'Le fichier doit être un PDF de moins de 20 Mo.')
            else:
                facture = form.save(commit=False)
                facture.utilisateur = request.user
                facture.save()
                form.save_m2m()
                return redirect('liste_factures')
    else:
        form = FactureForm()
    return render(request, 'montapp/upload_facture.html', {'form': form})

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document ajouté avec succès.')
            return redirect('document_list')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = DocumentForm()  # Créez le formulaire ici pour les requêtes GET

    return render(request, 'montapp/documents.html', {'form': form})

class DocumentListView(ListView):
    model = Document
    template_name = 'montapp/document_list.html'
    context_object_name = 'documents'
    ordering = ['-uploaded_at']

def statistiques_utilisateur(request):
    # Récupérez les données d'événements
    evenements = Evenement.objects.all()

    # Créez un dictionnaire pour stocker les statistiques par utilisateur et par année
    stats = {}

    # Parcourez les événements et calculez le nombre de jours par utilisateur et par année
    for evenement in evenements:
        utilisateur = evenement.utilisateur.username
        date_debut = evenement.date_debut
        date_fin = evenement.date_fin

        # Calculez la durée de l'événement en jours
        duree = (date_fin - date_debut).days

        # Extrayez l'année de l'événement
        annee = date_debut.year

        # Créez un dictionnaire pour stocker les statistiques par année pour chaque utilisateur
        if utilisateur not in stats:
            stats[utilisateur] = {}

        # Ajoutez la durée à l'année correspondante pour l'utilisateur
        if annee not in stats[utilisateur]:
            stats[utilisateur][annee] = 0
        stats[utilisateur][annee] += duree

    return JsonResponse(stats)

@require_POST
def create_evenement(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        Evenement.objects.create(
            utilisateur=request.user,
            titre=data['title'],
            date_debut=data['start'],
            date_fin=data['end'],
            couleur='#FF5733'  # Exemple de couleur, à adapter selon vos besoins
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def get_evenements(request):
    evenements = Evenement.objects.all()
    evenements_data = [{
        'title': ev.titre,
        'start': ev.date_debut,
        'end': ev.date_fin,
        'color': ev.couleur
    } for ev in evenements]
    return JsonResponse(evenements_data, safe=False)

def planning_url_view(request):
    return render(request, 'montapp/planning.html')

@login_required
def documents_url_view(request):
    return render(request, 'montapp/documents.html')

def infos(request):
    return render(request, 'montapp/infos.html')

def factures_url_view(request):
    return render(request, 'montapp/factures.html')

def reset_password_view(request):
    # Logique de la vue pour réinitialiser le mot de passe
    return render(request, 'montapp/reset_pwd.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def accueil_view(request):
    return render(request, 'montapp/accueil.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accueil')
            else:
                # Gérer l'échec de la connexion
                pass
    else:
        form = LoginForm()
    return render(request, 'montapp/login.html', {'form': form})


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Réinitialisation du mot de passe demandée"
                email_template_name = "montapp/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': 'exemple.com',  # Remplacer par le nom de domaine de votre site
                    'site_name': 'MonSite',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email_content = render_to_string(email_template_name, c)
                send_mail(subject, email_content, 'noreply@exemple.com', [user.email], fail_silently=False)
            return redirect("password_reset_done")
    return render(request, "montapp/reset_pwd.html")