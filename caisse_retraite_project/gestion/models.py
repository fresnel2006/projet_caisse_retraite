from django.db import models

class Adherent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    numero_securite_sociale = models.CharField(max_length=15, unique=True, help_text="Numéro de sécurité sociale unique")
    date_adhesion = models.DateField(auto_now_add=True) # La date est ajoutée automatiquement à la création

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Adhérent"
        ordering = ['nom', 'prenom'] # Ordonner les adhérents par nom par défaut

class Cotisation(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_versement = models.DateField()
    # Clé étrangère vers l'adhérent. Si l'adhérent est supprimé, ses cotisations le sont aussi.
    # related_name='cotisations' permet d'accéder aux cotisations depuis un objet Adherent (ex: mon_adherent.cotisations.all())
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE, related_name='cotisations')

    def __str__(self):
        return f"Cotisation de {self.montant}€ pour {self.adherent} le {self.date_versement}"

    class Meta:
        ordering = ['-date_versement'] # Ordonner de la plus récente à la plus ancienne
