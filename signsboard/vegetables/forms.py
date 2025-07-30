from django import forms
from .models import DeliverySlot

class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        max_length=500
    )
    delivery_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=15
    )
    delivery_slot = forms.ModelChoiceField(
        queryset=DeliverySlot.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    special_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )
