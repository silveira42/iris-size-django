from django.shortcuts import render, redirect
from .models import iGlobal
from .api.methods import *

# Create your views here.
def home(request):
    iglobals = iGlobal.objects.all()

    # handle filters
    database = request.GET.get("database")#, request.GET.get("fglobal")

    if database:# or fglobal:
        iglobals = iglobals.filter(database__icontains=database)#.filter(name__icontains=fglobal)
    else:
        database=""

    return render(request, "index.html", {"iglobals": iglobals, "database": database})#, "fglobal":fglobal})


def update(request):
    iGlobal.objects.all().delete()
    databaseList = getAllDatabaseDirectories()

    for database in databaseList:
        globalList = getGlobalsList(database)

        for glob in globalList:
            used, allocated = getGlobalSize(database, glob)
            iGlobal.objects.create(database=database, name=glob, realsize=used, allocatedsize=allocated)

    return redirect(home)
