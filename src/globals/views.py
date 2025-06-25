from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.core import serializers
from .models import iGlobal
from .api.methods import *


def handle_filters(request):
    iglobals = iGlobal.objects.all()
    fdatabase, fglobal, fsize, fallocated = request.GET.get("fdatabase"), request.GET.get("fglobal"), request.GET.get("fsize"), request.GET.get("fallocated")

    if fdatabase:
        iglobals = iglobals.filter(Q(database__contains=fdatabase))
    else:
        fdatabase=""
    if fglobal:
        iglobals = iglobals.filter(Q(name__contains=fglobal))
    else:
        fglobal=""
    if fsize:
        if fsize >=0:
            iglobals = iglobals.filter(Q(realsize__gte=fsize))
        else:
            iglobals = iglobals.filter(Q(realsize__lte=fsize))
    if fallocated:
        if fallocated >=0:
            iglobals = iglobals.filter(Q(allocatedsize__gte=fallocated))
        else:
            iglobals = iglobals.filter(Q(allocatedsize__lte=fallocated))


    return iglobals, fdatabase, fglobal, fsize, fallocated

# Create your views here.
def home(request):
    iglobals, fdatabase, fglobal, fsize, fallocated = handle_filters(request)
    sumSize = iglobals.aggregate(Sum("realsize"))
    sumAllocated = iglobals.aggregate(Sum("allocatedsize"))

    return render(request, "index.html", {"iglobals": iglobals, "fdatabase": fdatabase, "fglobal":fglobal, "fsize": fsize, "fallocated": fallocated, "sumSize": sumSize, "sumAllocated": sumAllocated})


def update(request):
    iGlobal.objects.all().delete()
    dbReturn =  getAllDatabaseDirectories()
    databaseList, databaseName = dbReturn[0], dbReturn[1]
    for i in range(len(databaseList)):
        gReturn = getGlobalsList(databaseList[i], databaseName[i])
        globalList, tableList = gReturn[0], gReturn[1]
        for j in range(len(globalList)):
            sReturn= getGlobalSize(databaseList[i], globalList[j])
            used, allocated = sReturn[0], sReturn[1]
            iGlobal.objects.create(database=databaseList[i], name=globalList[j], tablename=tableList[j], realsize=used, allocatedsize=allocated)

    return redirect(home)

import os
def export(request):
    iglobals = handle_filters(request)[0]
    cd = os.getcwd()
    xLanguage = request.GET.get("exportLanguage")

    if xLanguage == "CSV":
        with open(cd+"\\export.csv", "w") as file:
            for iglobal in iglobals:
                row = iglobal.database+", "+iglobal.name+", "+str(iglobal.realsize)+", "+str(iglobal.allocatedsize)+"\n"
                file.write(row)
    elif xLanguage == "XML":
        with open(cd+"\\export.xml", "w") as file:
            iglobals = serializers.serialize('xml', iglobals)
            file.write(iglobals)
    elif xLanguage == "JSON":
        with open(cd+"\\export.json", "w") as file:
            iglobals = serializers.serialize('json', iglobals)
            file.write(iglobals)

    return redirect(home)
