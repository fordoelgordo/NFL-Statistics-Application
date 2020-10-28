from django.shortcuts import render
from passing import forms

import pandas as pd
import pathlib

_DATA_PATH = 'static/archive/'
_DROP_FRAME = [ 
    'passId',
    'playId',
    'teamId',
    'playerId',
    'passAtt',
    'passComp',
    'passTd',
    'passInt',
    'passIntTd',
    'passSack',
    'passSackYds',
    'passHit',
    'passDef',
    'passNull',
    ]

_RENAME_COLS = {
    'passPosition' : 'Pass Position',
    'passOutcomes' : 'Pass Outcomes',
    'passDirection' : 'Pass Direction',
    'passDepth' : 'Pass Depth',
    'passLength' : 'Pass Length'
    }

if pathlib.Path('static/archive/').exists():
    # Read associated csv files
    pass_df = pd.read_csv(f'{_DATA_PATH}passer.csv')
    players_df = pd.read_csv(f'{_DATA_PATH}players.csv', usecols=['playerId', 'nameFirst', 'nameLast'])
    plays_df = pd.read_csv(f'{_DATA_PATH}plays.csv', usecols=['playId', 'gameId'])
    games_df = pd.read_csv(f'{_DATA_PATH}games.csv', usecols=['gameId', 'season', 'week', 'gameDate'])

# Create your views here.
def pass_page(request):
    form = forms.PassingForm()

    # Set holding variables
    pass_dict = pd.DataFrame()

    if request.method == "POST": # Means someone filled out our form
        form = forms.PassingForm(request.POST)

        if form.is_valid():
            # Get values from form
            player_name = form.cleaned_data.get('player_name').title()
            passing_year = form.cleaned_data.get('passing_year')
            passing_outcome = form.cleaned_data.get('passing_outcome')
            passing_length = form.cleaned_data.get('passing_length')

            if player_name:
                name_filter = players_df.loc[(players_df['nameFirst'] == player_name.split()[0]) & (players_df['nameLast'] == player_name.split()[1])]
                if len(name_filter) == 0:
                    return render(request,'passing/passing.html', {'form': form, 'empty': 'Player Does Not Exist!'})

              
            if player_name != "" and str(passing_year) == "None" and passing_outcome != "" and str(passing_length) != 'None':
                #print(1)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                        (pass_df['passOutcomes'].values == passing_outcome) & 
                                        (pass_df['passLength'].values == passing_length)]

            elif player_name != "" and str(passing_year) == "None" and passing_outcome == "" and str(passing_length) != 'None': 
                #print(2)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                        (pass_df['passLength'].values == passing_length)]

            elif player_name != "" and str(passing_year) == "None" and passing_outcome != '': 
                #print(3)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                        (pass_df['passOutcomes'].values == passing_outcome)]

            elif player_name != "" and str(passing_year) == "None":
                #print(4)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

            # If pass_dict has data
            if not pass_dict.empty:
                pass_dict.insert(0, 'First Name', player_name.split()[0])
                pass_dict.insert(1, 'Last Name', player_name.split()[1])
                pass_dict = pass_dict.drop(columns=_DROP_FRAME)
                pass_dict = pass_dict.rename(columns=_RENAME_COLS)
          

    if not pass_dict.empty:
        return render(request,'passing/passing.html', {'form': form, 'pass': pass_dict, 'columns' : pass_dict.columns})
        
    else:
        return render(request,'passing/passing.html', {'form': form})