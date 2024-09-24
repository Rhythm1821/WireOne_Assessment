from django import forms
from .models import PricingConfig

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = ['day_of_week', 'base_distance_price', 'base_distance_limit', 'additional_price_per_km', 'time_multiplier_factor', 'waiting_charge_per_minute', 'enabled']

    def clean(self):
        cleaned_data = super().clean()
        base_distance_price = cleaned_data.get('base_distance_price')
        additional_price_per_km = cleaned_data.get('additional_price_per_km')

        # Example validation: Ensure prices are positive
        if base_distance_price <= 0:
            self.add_error('base_distance_price', 'Base distance price must be positive.')

        if additional_price_per_km <= 0:
            self.add_error('additional_price_per_km', 'Additional price per km must be positive.')

        return cleaned_data
