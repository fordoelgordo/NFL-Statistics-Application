from django.shortcuts import render
from passing import forms
from static.team42libraries.csvtodict import csv_to_dict

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

pass_df = pd.DataFrame()
players_df = pd.DataFrame()
plays_df = pd.DataFrame()
games_df = pd.DataFrame()

if pathlib.Path('static/archive/').exists():
    # Read associated csv files
    pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
    players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)
    plays_df = csv_to_dict(f'{_DATA_PATH}plays.csv', 1)
    games_df = csv_to_dict(f'{_DATA_PATH}games.csv', 1)


# Create your views here.
def pass_page(request):
<<<<<<< Updated upstream
    form = forms.PassingForm()
    global pass_df, players_df, plays_df, games_df

    if pass_df.empty or players_df.empty or plays_df.empty or games_df.empty:
        pass_df = pd.read_csv(f'{_DATA_PATH}passer.csv')
        players_df = pd.read_csv(f'{_DATA_PATH}players.csv', usecols=['playerId', 'nameFirst', 'nameLast'])
        plays_df = pd.read_csv(f'{_DATA_PATH}plays.csv', usecols=['playId', 'gameId'])
        games_df = pd.read_csv(f'{_DATA_PATH}games.csv', usecols=['gameId', 'season', 'week', 'gameDate'])
=======
    global pass_df, players_df, plays_df, games_df

    if pass_df.empty or players_df.empty or plays_df.empty or games_df.empty:
        pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
        players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)
        plays_df = csv_to_dict(f'{_DATA_PATH}plays.csv', 1)
        games_df = csv_to_dict(f'{_DATA_PATH}games.csv', 1)
>>>>>>> Stashed changes

    # Set holding variables
    form = forms.PassingForm()
    analytics = forms.PassingAnalytics()
    context = {'form': form, 'analytics': analytics}

    if request.method == "POST": # Means someone filled out our form
        form = forms.PassingForm(request.POST)
        analytics = forms.PassingAnalytics(request.POST)

        if form.is_valid():
<<<<<<< Updated upstream
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

            elif player_name == "" and str(passing_year) != "None":
                #print(5)
                temp_df = pd.merge(pass_df, plays_df, on='playId')
                temp_df = pd.merge(temp_df, games_df, on='gameId')
                #print(games_df['season'].values)
                #pass_dict = pass_df.loc[(games_df['season'].values == int(passing_year))]
                pass_dict = temp_df
    
            # If pass_dict has data
            if not pass_dict.empty:
                #if player_name:
                    #pass_dict.insert(0, 'First Name', player_name.split()[0])
                    #pass_dict.insert(1, 'Last Name', player_name.split()[1])
                if passing_year:
                    pass_dict.insert(4, 'Year', int(passing_year))
                pass_dict = pass_dict.drop(columns=_DROP_FRAME)
                pass_dict = pass_dict.rename(columns=_RENAME_COLS)
          
=======
            context = parse_form_entries(request, form)
            context['analytics'] = analytics


        if analytics.is_valid():
            context = passing_analytics(request, analytics) 
            context['form'] = form

    
    return render(request,'passing/passing.html', context)


def parse_form_entries(request, form):
    pass_dict = pd.DataFrame()

    # Get values from form
    player_name = form.cleaned_data.get('player_name').title()
    passing_year = form.cleaned_data.get('passing_year')
    passing_outcome = form.cleaned_data.get('passing_outcome')
    passing_length = form.cleaned_data.get('passing_length')

    if player_name:
        player_name = player_name.split()
        first_name = player_name[0]

        if len(player_name) < 2:
            return {'form': form, 'empty': 'Last Name Not Entered!'}
>>>>>>> Stashed changes

        last_name = player_name[1]
        name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

        if len(name_filter) == 0:
            return {'form': form, 'empty': 'Player Does Not Exist!'}

      
    if player_name != "" and str(passing_year) == "None" and passing_outcome != "" and str(passing_length) != 'None':
        pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passOutcomes'].values == passing_outcome) & 
                                (pass_df['passLength'].values == passing_length)]

    elif player_name != "" and str(passing_year) == "None" and passing_outcome == "" and str(passing_length) != 'None': 
        pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passLength'].values == passing_length)]

    elif player_name != "" and str(passing_year) == "None" and passing_outcome != '': 
        pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passOutcomes'].values == passing_outcome)]

    elif player_name != "" and str(passing_year) == "None":
        pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

    # If pass_dict has data
    if not pass_dict.empty:
        pass_dict.insert(0, 'First Name', first_name)
        pass_dict.insert(1, 'Last Name', last_name)
        pass_dict = pass_dict.drop(columns=_DROP_FRAME)
        pass_dict = pass_dict.rename(columns=_RENAME_COLS)

    return {'form': form, 'pass': pass_dict, 'columns' : pass_dict.columns}


def passing_analytics(analytics, form):





    return {'form': form}