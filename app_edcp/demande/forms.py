from django import forms


class ValidateForm(forms.Form):
  """ Formulaire de validation de projet de réponse. """
  observations = forms.CharField(
    label='Observations', 
    required=False,
    widget=forms.Textarea(attrs={'rows': 3}),
  )