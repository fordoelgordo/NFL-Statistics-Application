from django.shortcuts import render
import pandas as pd
from pandasql import sqldf
from player_management import forms 
from nfl_site.libraries import conv_height

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
    player_pos = ''
    player_dob = ''
    player_college = ''
    player_height = ''
    player_weight = 0.0
    player_exists = False
    
    if request.method == "POST": # Means someone filled out our form
        form = forms.PlayerForm(request.POST)
        if form.is_valid(): 
            player_dict.clear()
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            player_pos = form.cleaned_data.get('player_pos')
            player_dob = form.cleaned_data.get('plyaer_dob')
            player_college = form.cleaned_data.get('player_college')
            player_height = form.cleaned_data.get('player_height')
            player_weight = form.cleaned_data.get('player_weight')
            
            # Filter the players.csv for the entered info
            player_first_name = "\'" + player_first_name + "\'"
            player_last_name = "\'" + player_last_name + "\'"
            # Set variable if player exists or not
            if player_first_name.strip('\'') in players.nameFirst.values and player_last_name.strip('\'') in players.nameLast.values:
                player_exists = True
            else:
                player_exists = False
            # Filter the players dataframe
            players_filtered = sqldf("SELECT playerid AS 'Player ID', nameFirst AS 'First Name', nameLast AS 'Last Name', position AS 'Position', college AS 'College', heightInches AS 'Height', weight AS 'Weight', dob AS 'DOB', homeCity AS 'City', homeState AS 'State', homeCountry AS 'Country' FROM players WHERE nameFirst = {} AND nameLast = {};".format(player_first_name, player_last_name), locals())
            df_dict = players_filtered.to_dict()
            df_rec = players_filtered.to_dict(orient='records')

    context = {'form': form, 'df_dict':df_dict, 'df_rec':df_rec, 'exists':player_exists}

    return render(request, 'player_management/player_management.html', context)
