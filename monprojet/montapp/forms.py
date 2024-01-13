from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Document, Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['fichier', 'montant', 'utilisateurs']  # Ajoutez d'autres champs si nécessaire
        widgets = {
            'montant': forms.NumberInput(attrs={'step': '0.01'}),
            'utilisateurs': forms.CheckboxSelectMultiple(attrs={'class': 'hidden-field'}),
        }
        utilisateurs = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False  # Pour permettre la désélection
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))

class DocumentForm(forms.ModelForm):
    class Meta: 
        model = Document
        fields = ['document_type', 'comment']

    # Utilisez des widgets spécifiques pour les champs document_type et comment
    # document_type = forms.ChoiceField(choices=Document.DOCUMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Définissez les choix pour document_type en utilisant les choix du modèle
        # self.fields['document_type'].choices = self.Meta.model.DOCUMENT_CHOICES