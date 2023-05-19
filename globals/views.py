from django.shortcuts import render, redirect
from .models import iGlobal

# Create your views here.
def home(request):
    iglobals = iGlobal.objects.all()
    return render(request, "index.html", {"iglobals": iglobals})