from django.shortcuts import render
from passing import forms
from static.team42libraries.csvtodict import csv_to_dict
from operator import itemgetter

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
#lays_df = pd.DataFrame()
#games_df = pd.DataFrame()

if pathlib.Path('static/archive/').exists():
    # Read associated csv files
    pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
    players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)
    #plays_df = csv_to_dict(f'{_DATA_PATH}plays.csv', 1)
    #games_df = csv_to_dict(f'{_DATA_PATH}games.csv', 1)

    pass_dict = pass_df.to_dict()


# Create your views here.
def pass_page(request):
    global pass_df, players_df #games_df, #plays_df

    if pass_df.empty or players_df.empty:
        pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
        players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)
        #plays_df = csv_to_dict(f'{_DATA_PATH}plays.csv', 1)
        #games_df = csv_to_dict(f'{_DATA_PATH}games.csv', 1)

    # Set holding variables
    form = forms.PassingForm()
    analytics = forms.PassingAnalytics()
    context = {'form': form, 'analytics': analytics}

    if request.POST.get('Search') == 'Search':
        form = forms.PassingForm(request.POST)
        if form.is_valid():
            context = parse_form_entries(form)
            context['analytics'] = analytics

    if request.POST.get('Retrieve') == 'Retrieve':
        analytics = forms.PassingAnalytics(request.POST)
        if analytics.is_valid():
            context = passing_analytics(analytics) 
            context['form'] = form

    return render(request,'passing/passing.html', context)


def parse_form_entries(form):
    results = pd.DataFrame()

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

        last_name = player_name[1]
        name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

        if len(name_filter) == 0:
            return {'form': form, 'empty': 'Player Does Not Exist!'}

      
    if player_name != "" and str(passing_year) == "None" and passing_outcome != "" and str(passing_length) != 'None':
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passOutcomes'].values == passing_outcome) & 
                                (pass_df['passLength'].values == passing_length)]

    elif player_name != "" and str(passing_year) == "None" and passing_outcome == "" and str(passing_length) != 'None': 
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passLength'].values == passing_length)]

    elif player_name != "" and str(passing_year) == "None" and passing_outcome != '': 
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passOutcomes'].values == passing_outcome)]

    elif player_name != "" and str(passing_year) == "None":
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

    # If results has data
    if not results.empty:
        results.insert(0, 'First Name', first_name)
        results.insert(1, 'Last Name', last_name)
        results = results.drop(columns=_DROP_FRAME)
        results = results.rename(columns=_RENAME_COLS)

    return {'form': form, 'pass': results, 'columns' : results.columns}


def passing_analytics(analytics):
    top_player_count = analytics.cleaned_data.get('top_player_count')

    # Get overall passing yards for each player without pandas
    top_player_dict = top_n_passing_yards(top_player_count)

    r_dict={}
    temp_df = pd.DataFrame()
    results = pd.DataFrame()

    for key, value in top_player_dict.items():
        r_dict = {
            'Player Name' : get_player_name(key),
            'Total Passing Length (Yards)': value
        }
        temp_df = pd.DataFrame(r_dict, index=[0])
        results = results.append(temp_df, ignore_index=True)

    return {'analytics': analytics, 'pass': results, 'columns' : results.columns}

# Analytics are done not using Pandas
def top_n_passing_yards(tp_count):
    total_passing_dict = {}
    for i in range(len(pass_dict['playerId'])):
        cell_val = pass_dict['passLength'][i]
        player_id = pass_dict['playerId'][i]
        if cell_val:

            if player_id in total_passing_dict:
                total_passing_dict[player_id] += int(cell_val)
            else:
                total_passing_dict[player_id] = int(cell_val)


    passing_yards_desc = sorted(total_passing_dict.items(), key=itemgetter(1), reverse=True)
    # get the top n records from list and cast into a dictionary
    n_records = dict(passing_yards_desc[:tp_count])

    return n_records


def get_player_name(player_id):
    return players_df.loc[(players_df['playerId'] == player_id)]['nameFull'].values[0]