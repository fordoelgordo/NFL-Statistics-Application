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
    return render(request,'passing/passing.html')

'''
Author: FSt.J
Code Comments: adding relative path variable to point to the directory location of my NFL datasets.
               For me, they're one directory above our project directory in a folder called nfl_data
'''
'''
# NFL Data relative path
data_path = '../../nfl_data/'

# Function to convert decimal height to cleaner form
def conv_height(h):
    ft = int(divmod(h,12)[0])
    inch = round(int(divmod(h,12)[1]),0)
    if h == 0 or h == "" or h == " ":
        return ""
    else:
        return str(ft)+"'"+str(inch)+"\""

# Define a dict to map combine event header to clean name
COMBINE_DICT = {
    '': '', # Provide the option to not select a combine measurement
    'combineArm': 'Arm Length',
    'combine40yd': '40-yard dash',
    'combineVert': 'Vertical jump',
    'combineBench': 'Bench Press',
    'combineShuttle': 'Shuttle drill',
    'combineBroad': 'Broad Jump',
    'combine3cone': '3-Cone Drill',
    'combine60ydShuttle': '60-yard shuttle',
    'combineWonderlic':'Wonderlic',
}

# response/combine page rendering
def combine_page(request):
    form = forms.CombineForm()
    #data = []
    df_dict = []
    df_rec = []

    # Read in combine.csv dataset
    combine = pd.read_csv(data_path + 'combine.csv')
    combine['combineHeightConv'] = combine['combineHeight'].apply(lambda x: conv_height(x))

    # Set holding variables
    player_dict = {} # Store the player's ID and associated combine statistic
    player_first_name = ''
    player_last_name = ''
    combine_year = 0
    combine_event = ''
    combine_pos = ''

    if request.method == "POST": # Means someone filled out our form
        form = forms.CombineForm(request.POST)
        if form.is_valid(): 
            player_dict.clear()
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            combine_year = form.cleaned_data.get('combine_year')
            combine_event = form.cleaned_data.get('combine_event')
            combine_pos = form.cleaned_data.get('combine_pos')
            
            # Now we need to filter the combine data based on the values entered
            if player_first_name != "" and player_last_name != "" and str(combine_year) == "None" and combine_event != "":
                # Display player and combine event for selected event
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['nameLast'] == player_last_name) 
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college',combine_event]]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    COMBINE_DICT[combine_event]
                ]
            elif player_first_name != "" and player_last_name != "" and str(combine_year) == "None" and combine_event == "":
                # Display regular stats for just a selected player
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['nameLast'] == player_last_name)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event == "":
                # Display players in the combine for selected combine year
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year) 
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event == "" and combine_pos != "":
                # Display players in the combine for selected combine year and position group
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year) &
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event != "" and combine_pos == "":
                # Display players in the combine for the selected event for the selected year
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year)
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight', combine_event]]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                    COMBINE_DICT[combine_event]
                ]
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event != "" and combine_pos != "":
                # Display players in the combine for the selected event, position group, and year
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year) &
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight', combine_event]]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                    COMBINE_DICT[combine_event]
                ]
            df_dict = combine_filtered.to_dict()
            df_rec = combine_filtered.to_dict(orient='records')
                    
    #context = {'form':form, 'data':data}
    context = {'form': form, 'df_dict':df_dict, 'df_rec':df_rec}

    return render(request, 'combine/combine.html', context)
'''