from django import forms
from .models import Adherent, Cotisation

class AdherentForm(forms.ModelForm):
    class Meta:
        model = Adherent
        # On choisit les champs à afficher dans le formulaire
        fields = ['nom', 'prenom', 'date_naissance', 'numero_securite_sociale']
        # On peut personnaliser les widgets pour avoir un calendrier par exemple
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class CotisationForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['montant', 'date_versement']
        widgets = {
            'date_versement': forms.DateInput(attrs={'type': 'date'}),
        }
