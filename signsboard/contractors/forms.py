from django import forms
from .models import ContractorBooking

class ContractorBookingForm(forms.ModelForm):
    class Meta:
        model = ContractorBooking
        fields = [
            'project_title', 'project_description', 'estimated_duration',
            'budget', 'contact_phone', 'project_address', 'preferred_start_date'
        ]
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estimated_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'project_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preferred_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
