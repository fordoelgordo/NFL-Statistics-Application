from django.shortcuts import render
import pandas as pd
import pathlib
import numpy as np
from pandasql import sqldf
from standings import forms
from nfl_site.libraries import conv_height, getIndexes
from datetime import date, datetime

# Create your views here.
'''
Author: FSt.J
Code Comments: return NFL win-loss statistics to the user
'''
# NFL Data relative path
data_path = 'static/archive/'

# Global Variables

# Check if the csv path exists
if pathlib.Path(data_path).exists():
    True

# response/combine page rendering
def standings(request):
    year_form = forms.YearForm
    
    # Set holding variables
    submit = False
    year_val = 0

    if request.method == "POST": # Means someone filled out our player_form
        year_form = forms.YearForm(request.POST)
        if year_form.is_valid():
            submit = True
            year_val = year_form.cleaned_data.get('year_val')
            print(year_val)

    if request.POST.get('Division') == 'Division':
        print("Division button clicked")

    if request.POST.get('Conference') == 'Conference':
        print("Conference button clicked")

    if request.POST.get('League') == 'League':
        print("League button pressed")
        
    context = {'year_form': year_form, 'submit':submit}
    return render(request, 'standings/standings.html', context)