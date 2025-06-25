from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.core import serializers
from .models import iProcess
from .api.methods import getProcessList


def handle_filters(request):
    iprocesses = iProcess.objects.all()
    # fdatabase, fglobal, fsize, fallocated = request.GET.get("fdatabase"), request.GET.get("fglobal"), request.GET.get("fsize"), request.GET.get("fallocated")

    # if fdatabase:
    #     iprocesses = iprocesses.filter(Q(database__contains=fdatabase))
    # else:
    #     fdatabase=""
    # if fglobal:
    #     iprocesses = iprocesses.filter(Q(name__contains=fglobal))
    # else:
    #     fglobal=""
    # if fsize:
    #     if fsize >=0:
    #         iprocesses = iprocesses.filter(Q(realsize__gte=fsize))
    #     else:
    #         iprocesses = iprocesses.filter(Q(realsize__lte=fsize))
    # if fallocated:
    #     if fallocated >=0:
    #         iprocesses = iprocesses.filter(Q(allocatedsize__gte=fallocated))
    #     else:
    #         iprocesses = iprocesses.filter(Q(allocatedsize__lte=fallocated))


    return iprocesses

# Create your views here.
def home(request):
    iprocesses = handle_filters(request)

    return render(request, "process.html", {"iprocesses": iprocesses})


def update(request):
    iProcess.objects.all().delete()
    processList = getProcessList()
    for i in range(len(processList)):
        process = processList[i]
        iProcess.objects.create(jobNumber=process["jobNumber"],pid=process["pid"],
                                osUserName=process["osUserName"],currentDevice=process["currentDevice"],
                                routine=process["routine"],state=process["state"],userName=process["userName"])
    return redirect(home)

import os
def export(request):
    iprocesses = handle_filters(request)[0]
    cd = os.getcwd()
    xLanguage = request.GET.get("exportLanguage")

    if xLanguage == "CSV":
        with open(cd+"\\export.csv", "w") as file:
            for iglobal in iprocesses:
                row = iglobal.database+", "+iglobal.name+", "+str(iglobal.realsize)+", "+str(iglobal.allocatedsize)+"\n"
                file.write(row)
    elif xLanguage == "XML":
        with open(cd+"\\export.xml", "w") as file:
            iprocesses = serializers.serialize('xml', iprocesses)
            file.write(iprocesses)
    elif xLanguage == "JSON":
        with open(cd+"\\export.json", "w") as file:
            iprocesses = serializers.serialize('json', iprocesses)
            file.write(iprocesses)

    return redirect(home)
