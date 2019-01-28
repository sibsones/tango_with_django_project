from django.shortcuts import render
from django.http import HttpResponse

# Templates can be seen as scaffolding

# Create your views here.

def index(request):  # The view itself
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': "Rango says this is the about page!"}
    
    return render(request, 'rango/about.html', context=context_dict)
