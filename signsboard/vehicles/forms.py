from django import forms
from .models import VehicleBooking, Vehicle

class VehicleBookingForm(forms.ModelForm):
    class Meta:
        model = VehicleBooking
        fields = [
            'vehicle', 'booking_type', 'pickup_location', 'pickup_date', 'pickup_time',
            'dropoff_location', 'return_date', 'return_time', 'contact_phone',
            'passenger_count', 'special_requirements', 'estimated_distance_km',
            'estimated_duration_hours'
        ]
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'booking_type': forms.Select(attrs={'class': 'form-control'}),
            'pickup_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'dropoff_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'passenger_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(is_available=True)
