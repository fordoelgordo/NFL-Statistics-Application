from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.views import generic

import csv
import pandas as pd
import json # use to convert pandas dataframe into json object which we can use in html
from itertools import islice

from response import forms # Import forms module from response app

# Create your views here.
# Commenting this code out, these were for v1.1 of our site
'''
def index(request):
    my_dict = {'insert_me':"Now I am coming from response/index.html"}
    return render(request, 'response/index.html', context=my_dict) # Uses the index.html template with the my_dict variable
    
def click_button(request):
    my_dict = {'value': "Now I am coming from response/button_click.html"}
    return render(request, 'response/click_button.html', context=my_dict)
'''


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

'''
Author: FSt.J
Code Comments: adding relative path variable to point to the directory location of my NFL datasets.
               For me, they're one directory above our project directory in a folder called nfl_data
'''
# NFL Data relative path
data_path = '../../nfl_data/'

# FSt.J adding button to get to the combine page
def combine_page(request):
    form = forms.CombineForm()
    data = []

    # Read in combine.csv dataset
    combine = pd.read_csv(data_path + 'combine.csv')

    # Set holding variables
    player_dict = {} # Store the player's ID and associated combine statistic
    player_first_name = ''
    player_last_name = ''
    combine_year = 0
    combine_event = ''

    if request.method == "POST": # Means someone filled out our form
        form = forms.CombineForm(request.POST)
        if form.is_valid(): 
            player_dict.clear()
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            combine_year = form.cleaned_data.get('combine_year')
            combine_event = form.cleaned_data.get('combine_event')
            print(player_first_name != "")
            print(player_last_name != "")
            print(str(combine_year) == "None")
            print(combine_event == "")

            # Now we need to filter the combine data based on the values entered
            if player_first_name != "" and player_last_name != "" and str(combine_year) != "None" and combine_event != "":
                # All 4 fields have been entered, filter the data appropriately
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['nameLast'] == player_last_name) &
                        (combine['combineYear'] == combine_year)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college',combine_event]]
                json_records = combine_filtered.reset_index().to_json(orient ='records')  
                data = json.loads(json_records)
            elif player_first_name != "" and player_last_name != "" and str(combine_year) == "None" and combine_event == "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['nameLast'] == player_last_name)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college']]
                json_records = combine_filtered.reset_index().to_json(orient ='records')  
                data = json.loads(json_records)
    
    context = {'form':form, 'data':data}
    
    return render(request, 'response/combine.html', context)
