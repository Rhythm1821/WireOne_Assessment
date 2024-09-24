from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_pricing_config, name='create_pricing_config'),
    path('calculate_price/',views.calculate_price,name='calculate_price'),
]
