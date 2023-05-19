from django.shortcuts import render, redirect
from .models import iGlobal
from .api.methods import *

# Create your views here.
def home(request):
    iglobals = iGlobal.objects.all()
    return render(request, "index.html", {"iglobals": iglobals})

def update(request):
    iGlobal.objects.all().delete()
    databaseList = getAllDatabaseDirectories()
    for database in databaseList:
        globalList = getGlobalsList(database)
        for glob in globalList:
            globSize = getGlobalSize(database, glob)
            allocatedSize = getGlobalAllocatedSize(database, glob)
            iGlobal.objects.create(database=database, name=glob, realsize=globSize, allocatedsize=allocatedSize)

    return redirect(home)
