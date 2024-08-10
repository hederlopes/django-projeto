from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def contato(request):
    return HttpResponse('<b>CONTATO</b>')


def sobre(request):
    return HttpResponse('<b>SOBRE</b>')