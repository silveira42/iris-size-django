from django.shortcuts import render, redirect
from .models import iGlobal
from .api.methods import *

# Create your views here.
def home(request):
    iglobals = iGlobal.objects.all()
    print(iglobals)
    return render(request, "index.html", {"iglobals": iglobals})

def update(request):
    iGlobal.objects.all().delete() #TODO: CHANGE THIS TO A PROPER UPDATE
    databaseList = getAllDatabaseDirectories()
    for database in databaseList:
        globalList = getGlobalsList(database)
        for glob in globalList:
            used, allocated = getGlobalSize(database, glob)
            iGlobal.objects.create(database=database, name=glob, realsize=used, allocatedsize=allocated)

    return redirect(home)
