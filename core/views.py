# core/views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'core/index.html') # Aici referențiem 'core/index.html'