from rest_framework.response import Response
from decimal import Decimal
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.views import APIView

from .models import PricingConfig, PricingConfigLog
from .forms import PricingConfigForm

class CalculatePriceView(APIView):
    def post(self, request):
        # Getting data from the request
        distance_traveled = Decimal(request.data.get('distance'))
        ride_time = Decimal(request.data.get('time'))
        waiting_time = Decimal(request.data.get('waiting_time'))
        day_of_week = request.data.get('day_of_week')
        
        # Fetching the active pricing configuration for the given day
        config = PricingConfig.objects.filter(day_of_week=day_of_week, enabled=True).first()
        if not config:
            return Response({"error": "Pricing configuration not found"}, status=404)
        
        # Calculating additional distance
        additional_distance = max(0, distance_traveled - config.base_distance_limit)
        
        # Calculating the price
        price = (config.base_distance_price + (additional_distance * config.additional_price_per_km)) + \
                (ride_time * config.time_multiplier_factor) + \
                (waiting_time * config.waiting_charge_per_minute)
        
        return Response({"price": price})





class CreatePricingConfigView(LoginRequiredMixin, CreateView):
    model = PricingConfig
    form_class = PricingConfigForm
    template_name = 'create_pricing_config.html'
    success_url = reverse_lazy('create_pricing_config')

    def form_valid(self, form):
        config = form.save(commit=False)
        changed_data = form.changed_data

        for field_name in changed_data:
            old_value = form.initial.get(field_name)
            new_value = form.cleaned_data.get(field_name)

            print(f'Field: {field_name}, Old Value: {old_value}, New Value: {new_value}')

        # Save the PricingConfig instance to the database
        config.save()

        # After the config is saved, create the log entry
        PricingConfigLog.objects.create(
            config=config,
            modified_by=self.request.user.username,
            action='Created',
            changes=f'Field: {field_name}, Old Value: {old_value}, New Value: {new_value}'
        )

        messages.success(self.request, 'Data submitted successfully!')
        return super().form_valid(form)