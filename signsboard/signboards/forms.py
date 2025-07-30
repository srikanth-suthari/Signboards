from django import forms
from .models import SignboardOrder, SignboardType, SignboardSize, SignboardFinish

class SignboardQuoteForm(forms.ModelForm):
    class Meta:
        model = SignboardOrder
        fields = [
            'business_name', 'signboard_type', 'size', 'finish',
            'text_content', 'font_preferences', 'color_preferences',
            'logo_upload', 'design_file', 'special_requirements',
            'installation_required', 'installation_address', 'contact_phone',
            'preferred_installation_date', 'urgency'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'signboard_type': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'finish': forms.Select(attrs={'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'font_preferences': forms.TextInput(attrs={'class': 'form-control'}),
            'color_preferences': forms.TextInput(attrs={'class': 'form-control'}),
            'logo_upload': forms.FileInput(attrs={'class': 'form-control'}),
            'design_file': forms.FileInput(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'installation_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'installation_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_installation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
        }
