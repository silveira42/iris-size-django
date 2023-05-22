from django.shortcuts import render, redirect
from .models import iGlobal
from .api.methods import *


def handle_filter(request):
    iglobals = iGlobal.objects.all()
    # handle filters
    fdatabase, fglobal, fsize, fallocated = request.GET.get("fdatabase"), request.GET.get("fglobal"), request.GET.get("fsize"), request.GET.get("fallocated")

    if not fdatabase: fdatabase=""
    if not fglobal: fglobal=""

    if fdatabase or fglobal:
        iglobals = iglobals.filter(database__icontains=fdatabase).filter(name__icontains=fglobal)

    if type(fsize) != type(None):
        fsize = float(fsize)
        if fsize>=0:
            iglobals = iglobals.filter(realsize__gte=fsize)
        else:
            iglobals = iglobals.filter(realsize__lte=-fsize)

    if type(fallocated) != type(None):
        fallocated = float(fallocated)
        if fallocated>=0:
            iglobals = iglobals.filter(realsize__gte=fallocated)
        else:
            iglobals = iglobals.filter(realsize__lte=-fallocated)

    return iglobals, fdatabase, fglobal, fsize, fallocated

# Create your views here.
def home(request):
    iglobals = iGlobal.objects.all()
    fdatabase, fglobal, fsize, fallocated = request.GET.get("fdatabase"), request.GET.get("fglobal"), request.GET.get("fsize"), request.GET.get("fallocated")

    if not fdatabase: fdatabase=""
    if not fglobal: fglobal=""

    if fdatabase or fglobal:
        iglobals = iglobals.filter(database__icontains=fdatabase).filter(name__icontains=fglobal)

    if fsize:
        fsize = float(fsize)
        if fsize>=0:
            iglobals = iglobals.filter(realsize__gte=fsize)
        else:
            iglobals = iglobals.filter(realsize__lte=-fsize)

    if fallocated:
        fallocated = float(fallocated)
        if fallocated>=0:
            iglobals = iglobals.filter(allocatedsize__gte=fallocated)
        else:
            iglobals = iglobals.filter(allocatedsize__lte=-fallocated)
    #iglobals, fdatabase, fglobal, fsize, fallocated = handle_filter(request)
    return render(request, "index.html", {"iglobals": iglobals, "fdatabase": fdatabase, "fglobal":fglobal, "fsize": fsize, "fallocated": fallocated})


def update(request):
    iGlobal.objects.all().delete()
    databaseList = getAllDatabaseDirectories()

    for database in databaseList:
        globalList = getGlobalsList(database)

        for glob in globalList:
            used, allocated = getGlobalSize(database, glob)
            iGlobal.objects.create(database=database, name=glob, realsize=used, allocatedsize=allocated)

    return redirect(home)
