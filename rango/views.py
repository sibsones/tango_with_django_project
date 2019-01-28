from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):  # The view itself
    return HttpResponse('''Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>''') # A view should contain at least one argument

def about(request):
    return HttpResponse('''Rango says here is the about page <br/> <a href='/rango/'>Index</a>''')
