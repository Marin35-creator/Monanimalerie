from django import forms
from .models import Animal

class AssignEquipementForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['equipement']  # N'incluez que le champ 'equipement'

