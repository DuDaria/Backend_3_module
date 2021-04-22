from django.shortcuts import render
from django.http import HttpResponse

def index1(request):
    return HttpResponse("Hello world!")

def index2(request):
    return HttpResponse("Hello New world!")
