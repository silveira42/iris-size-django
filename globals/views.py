from django.shortcuts import render, redirect
from .models import Global

# Create your views here.
def home(request):
    return render(request, "index.html")