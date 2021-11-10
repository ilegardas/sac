from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def bienvenido(request):
    return HttpResponse('Hola Mundo desde django')
def despedirse(request):
    return HttpResponse('Despedirse desde django')
def contacto(reguest):
    return HttpResponse('Telefono: 6144730104 Email: contacto@ivanlegarda.com')

