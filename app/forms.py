from django import forms
from .models import Roomtype

class AvailableForm(forms.ModelForm):
    class Meta:
        model = Roomtype
        fields = ['name','people','price']
