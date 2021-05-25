from django import forms
from .models import Roomtype,Reservation

class AvailableForm(forms.ModelForm):
    class Meta:
        model = Roomtype
        fields = ['name','people','price']

class BookingForm(forms.ModelForm):
    class Meta:
        model: Reservation
        fields = ['checkin','checkout','state','adults','children','customer','room']
