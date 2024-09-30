from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreatePricingConfigView.as_view(), name='create_pricing_config'),
    path('calculate_price/',views.CalculatePriceView.as_view(),name='calculate_price'),
]
