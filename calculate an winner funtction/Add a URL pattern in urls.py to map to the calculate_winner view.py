from django.urls import path
from . import views

urlpatterns = [
    path('calculate-winner/', views.calculate_winner, name='calculate_winner'),
]
