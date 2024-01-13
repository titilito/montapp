from django.db import models
from django.contrib.auth.models import User

class Facture(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    fichier = models.FileField(upload_to='factures/')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factures')
    utilisateurs = models.ManyToManyField(User, blank=True, related_name='factures_associees')
    date_depot = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Facture {self.id} de {self.utilisateur}"

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    DOCUMENT_CHOICES = [
        ('Compte rendu', 'Compte rendu'),
        ('Règlement', 'Règlement'),
        ('Avenant', 'Avenant'),
        ('Autre', 'Autre'),
    ]
    document_type = models.CharField(max_length=255, choices=DOCUMENT_CHOICES)
    comment = models.TextField()
    #uploaded_file = models.FileField(upload_to='files_storage/')
    def __str__(self):
        return self.document_type
    def get_absolute_url(self):
        return reverse('document_view', args=[self.id])

class Evenement(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField()
    couleur = models.CharField(max_length=7)  # Stocke la couleur au format HEX, par exemple, #FF5733