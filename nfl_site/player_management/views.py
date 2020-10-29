from django.shortcuts import render
import pandas as pd
import pathlib
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
output_path = 'static/saves/'

players = pd.DataFrame()
players_filtered = pd.DataFrame()

if pathlib.Path('static/archive/').exists():
    #Read in combine.csv dataset
    players = pd.read_csv(data_path + 'players.csv')

# response/combine page rendering
def player_management(request):
    player_form = forms.PlayerForm()
    edit_form = forms.EditForm()
    df_dict = []
    df_rec = []
    global players
    global players_filtered

    if players.empty:
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
    submit = False
    
    if request.method == "POST": # Means someone filled out our player_form
        player_form = forms.PlayerForm(request.POST)
        if player_form.is_valid():
            submit = True
            player_dict.clear()
            player_first_name = player_form.cleaned_data.get('player_first_name').title()
            player_last_name = player_form.cleaned_data.get('player_last_name').title()
        
            
            # Filter the players.csv for the entered info
            player_first_name = "\'" + player_first_name + "\'"
            player_last_name = "\'" + player_last_name + "\'"
 
            # Set variable if player exists or not
            if player_first_name.strip('\'') in players.nameFirst.values and player_last_name.strip('\'') in players.nameLast.values:
                player_exists = True
            else:
                player_exists = False
 
            # Filter the players dataframe
            players_filtered = sqldf(f"SELECT playerid AS 'Player ID', nameFirst AS 'First Name', nameLast AS 'Last Name', position AS 'Position', college AS 'College', heightInches AS 'Height', weight AS 'Weight', dob AS 'DOB', homeCity AS 'City', homeState AS 'State', homeCountry AS 'Country' FROM players WHERE nameFirst = {player_first_name} AND nameLast = {player_last_name};", globals())
            df_dict = players_filtered.to_dict()
            df_rec = players_filtered.to_dict(orient='records')

    if request.POST.get('Add Player') == 'Add_Player':
        edit_form = forms.EditForm(request.POST)
        if edit_form.is_valid():
            # ADD FIELD FOR PID IF > 1
            player_pos = edit_form.cleaned_data.get('player_pos')
            player_dob = edit_form.cleaned_data.get('player_dob')
            player_college = edit_form.cleaned_data.get('player_college')
            player_height = edit_form.cleaned_data.get('player_height')
            player_weight = edit_form.cleaned_data.get('player_weight')

        #check PID

    if request.POST.get('Edit Player') == 'Edit Player':
        edit_form = forms.EditForm(request.POST)
        if edit_form.is_valid():
            # ADD FIELD FOR PID IF > 1
            player_pos = edit_form.cleaned_data.get('player_pos')
            player_dob = edit_form.cleaned_data.get('player_dob')
            player_college = edit_form.cleaned_data.get('player_college')
            player_height = edit_form.cleaned_data.get('player_height')
            player_weight = edit_form.cleaned_data.get('player_weight')
        
        print(player_dob)

        if player_pos:
            players.loc[(players['playerId'].values == players_filtered['Player ID'].values[0], 'position')] = player_pos
        
        if player_dob:
            players.loc[(players['playerId'].values == players_filtered['Player ID'].values[0], 'dob')] = player_dob
        
        if player_college:
            players.loc[(players['playerId'].values == players_filtered['Player ID'].values[0], 'college')] = player_college

        if player_height:
            players.loc[(players['playerId'].values == players_filtered['Player ID'].values[0], 'heightInches')] = float(player_height)

        if player_weight:
            players.loc[(players['playerId'].values == players_filtered['Player ID'].values[0], 'weight')] = float(player_weight)

    if request.POST.get('Delete Player') == 'Delete Player':
        print("3")
        #DROP ROW with player name
            
    

    context = {'player_form': player_form, 'edit_form': edit_form, 'df_dict':df_dict, 'df_rec':df_rec, 'exists':player_exists, 'submit':submit}

    return render(request, 'player_management/player_management.html', context)
