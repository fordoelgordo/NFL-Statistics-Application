from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    my_dict = {'insert_me':"Now I am coming from response/index.html"}
    return render(request, 'response/index.html', context=my_dict) # Uses the index.html template with the my_dict variable
    
def click_button(request):
    my_dict = {'value': "Now I am coming from response/button_click.html"}
    return render(request, 'response/click_button.html', context=my_dict)