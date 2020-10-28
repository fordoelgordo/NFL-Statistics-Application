from django.shortcuts import render
import pandas as pd
from player_management import forms # Import forms module from response app
from pandasql import sqldf

# Create your views here.
'''
Author: FSt.J
Code Comments: adding relative path variable to point to the directory location of my NFL datasets.
               For me, they're one directory above our project directory in a folder called nfl_data
'''
# NFL Data relative path
data_path = 'static/archive/'

# response/combine page rendering
def player_management(request):
    form = forms.PlayerForm()
    df_dict = []
    df_rec = []

    # Read in combine.csv dataset
    players = pd.read_csv(data_path + 'players.csv')
    
    # Set holding variables
    player_dict = {} # Store the player's ID and associated combine statistic
    player_first_name = ''
    player_last_name = ''
    
    if request.method == "POST": # Means someone filled out our form
        form = forms.PlayerForm(request.POST)
        if form.is_valid(): 
            player_dict.clear()
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            
            # Filter the players.csv for the entered info
            player_first_name = "\'" + player_first_name + "\'"
            player_last_name = "\'" + player_last_name + "\'"
            players_filtered = sqldf("SELECT playerid, nameFirst, nameLast, position, college, heightInches, weight, dob, homeCity, homeState, homeCountry FROM players WHERE nameFirst = {} AND nameLast = {};".format(player_first_name, player_last_name), locals())
            df_dict = players_filtered.to_dict()
            df_rec = players_filtered.to_dict(orient='records')

    context = {'form': form, 'df_dict':df_dict, 'df_rec':df_rec}

    return render(request, 'player_management/player_management.html', context)
