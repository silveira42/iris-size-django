from django.shortcuts import render, redirect
from django.db.models import Q
from django.core import serializers
from .models import iGlobal
from .api.methods import *


def handle_filters(request):
    iglobals = iGlobal.objects.all()
    fdatabase, fglobal, fsize, fallocated = request.GET.get("fdatabase"), request.GET.get("fglobal"), request.GET.get("fsize"), request.GET.get("fallocated")

    if not fdatabase: fdatabase=""
    if not fglobal: fglobal=""

    q1 = Q(database__icontains=fdatabase)
    q2 = Q(name__icontains=fglobal)

    if fsize:
        fsize = float(fsize)
        if fsize>=0:
            q3 = Q(realsize__gte=fsize)
        else:
            q3 = Q(realsize__lte=-fsize)
    else:
        q3 = Q(realsize__gte=0)

    if fallocated:
        fallocated = float(fallocated)
        if fallocated>=0:
            q4 = Q(allocatedsize__gte=fallocated)
        else:
            q4 = Q(allocatedsize__lte=-fallocated)
    else:
        q4 = Q(allocatedsize__gte=0)

    iglobals = iglobals.filter(q1, q2, q3, q4)

    return iglobals, fdatabase, fglobal, fsize, fallocated

# Create your views here.
def home(request):
    iglobals, fdatabase, fglobal, fsize, fallocated = handle_filters(request)
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

import os
# def export(request):
#     iglobals = handle_filters(request)[0]
#     cd = os.getcwd()
#     with open(cd+"\\test.csv", "w") as file:
#         for iglobal in iglobals:
#             row = iglobal.database+", "+iglobal.name+", "+str(iglobal.realsize)+", "+str(iglobal.allocatedsize)+"\n"
#             file.write(row)

#     return redirect(home)


def export(request):
    iglobals = handle_filters(request)[0]
    cd = os.getcwd()
    with open(cd+"\\test.xml", "w") as file:
        iglobals = serializers.serialize('xml', iglobals)
        file.write(iglobals)

    return redirect(home)