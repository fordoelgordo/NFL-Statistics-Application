from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    my_dict = {'insert_me':"Now I am coming from response/index.html"}
    return render(request, 'response/index.html', context=my_dict) # Uses the index.html template with the my_dict variable