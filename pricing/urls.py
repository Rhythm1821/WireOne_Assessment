from django.urls import path
from . import views

urlpatterns = [
    path('calculate_price/',views.calculate_price,name='calculate_price'),
]
