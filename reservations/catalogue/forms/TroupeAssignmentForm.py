from django import forms
from catalogue.models import Troupe

class TroupeAssignmentForm(forms.Form):
    troupe = forms.ModelChoiceField(
        queryset=Troupe.objects.all(),
        required=True,
        label="Troupe",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
