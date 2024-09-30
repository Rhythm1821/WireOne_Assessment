from django import forms
from .models import PricingConfig

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = [
            'day_of_week',
            'base_distance_price',
            'base_distance_limit',
            'additional_price_per_km',
            'time_multiplier_factor',
            'waiting_charge_per_minute',
            'enabled',
        ]
        labels = {
            'day_of_week': 'Day of the Week',
            'base_distance_price': 'Distance Base Price (INR)',
            'base_distance_limit': 'Distance Limit (KM)',
            'additional_price_per_km': 'Additional Price per KM (INR)',
            'time_multiplier_factor': 'Time Multiplier Factor',
            'waiting_charge_per_minute': 'Waiting Charge per Minute (INR)',
            'enabled': 'Is Active?',
        }
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'base_distance_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'base_distance_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'additional_price_per_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'time_multiplier_factor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'waiting_charge_per_minute': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        base_distance_price = cleaned_data.get('base_distance_price')
        additional_price_per_km = cleaned_data.get('additional_price_per_km')

        if base_distance_price < 0:
            self.add_error('base_distance_price', "Base distance price cannot be negative.")
        if additional_price_per_km < 0:
            self.add_error('additional_price_per_km', "Additional price per km cannot be negative.")

        return cleaned_data
