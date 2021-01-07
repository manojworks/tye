from django.shortcuts import render
from django.http import HttpResponse


def list_all(request):
    return HttpResponse("List of all Taxonomies")