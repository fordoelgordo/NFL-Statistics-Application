from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.views import generic

import csv
from itertools import islice


# Create your views here.
def index(request):
    my_dict = {'insert_me':"Now I am coming from response/index.html"}
    return render(request, 'response/index.html', context=my_dict) # Uses the index.html template with the my_dict variable
    
def click_button(request):
    my_dict = {'value': "Now I am coming from response/button_click.html"}
    return render(request, 'response/click_button.html', context=my_dict)



# adding new functions here -- Eduardo v v v v
# View: As the name implies, it represents what you see while on your 
# browser for a web application or In the UI for a desktop application.

def home(request):
    return render(request,'response/home.html')

def rusher_page(request):
    return render(request,'response/rusher.html')

def catcher_page(request):
    return render(request,'response/catcher.html')

def passer_page(request):
    return render(request,'response/passer.html')
