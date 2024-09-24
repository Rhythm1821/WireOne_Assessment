from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PricingConfig
from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PricingConfig, PricingConfigLog
from .forms import PricingConfigForm
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

@api_view(['POST'])
def calculate_price(request):
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
def create_pricing_config(request):
    if request.method == 'POST':
        form = PricingConfigForm(request.POST)
        if form.is_valid():
            config=form.save()
            PricingConfigLog.objects.create(
                config=config,
                modified_by=request.user.username,
                action='Created'
            )
            messages.success(request, 'Data submitted successfully!')
            return redirect('create_pricing_config')
    else:
        form = PricingConfigForm()
    return render(request, 'create_pricing_config.html', {'form': form})
