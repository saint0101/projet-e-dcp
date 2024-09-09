from django import forms
from facturation.models import Paiement



class JustificatifPaiementForm(forms.ModelForm):
  
  class Meta:
    model = Paiement
    fields = ['montant', 'file_justificatif']