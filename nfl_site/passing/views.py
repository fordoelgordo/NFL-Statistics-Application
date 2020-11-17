from django.shortcuts import render
from passing import forms
from static.team42libraries.csvtodict import csv_to_dict
from operator import itemgetter

import pandas as pd
import pathlib
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

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


if pathlib.Path('static/archive/').exists():
    # Read associated csv files
    pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
    players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)


# Create your views here.
def pass_page(request):
    global pass_df, players_df  #games_df, #plays_df

    if pass_df.empty or players_df.empty or request.POST.get('Refresh Data') == 'Refresh Data':
        pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
        players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)

    # Set holding variables
    form = forms.PassingForm()
    analytics = forms.PassingAnalytics()
    context = {'form': form, 'analytics': analytics}

    if request.POST.get('Search') == 'Search':
        form = forms.PassingForm(request.POST)
        if form.is_valid():
            context = parse_form_entries(form)
            context['analytics'] = analytics

    if request.POST.get('Show Table') == 'Show Table' or request.POST.get('Show Graph') == 'Show Graph' or request.POST.get('Show Scatter Plot') == 'Show Scatter Plot':
        analytics = forms.PassingAnalytics(request.POST)
        if analytics.is_valid():
            context = passing_analytics(analytics) 
            context['form'] = form
            context['exists'] = True

        if request.POST.get('Show Graph') == 'Show Graph':
            results = context['results']
            top_player_count = context['n_count']
            context['results'] = pd.DataFrame()

            fig = go.Figure(data=[
                go.Bar(name='Total Passing Length (Yards)', x=results['Player Name'], y=results['Total Passing Length (Yards)']),
                go.Bar(name='Total Times Passed (from csv)', x=results['Player Name'], y=results['Total Times Passed (from csv)'])
                ], 
                layout_title_text=f'Top {top_player_count} Players (Total Passing Yards)' )

            fig.update_layout(barmode='group')
            graph_div = plotly.offline.plot(fig, output_type="div")
            context['graph_div'] = graph_div

        if request.POST.get('Show Scatter Plot') == 'Show Scatter Plot':
            results = context['results']
            top_player_count = context['n_count']
            context['results'] = pd.DataFrame()

            fig = px.scatter(results, x="Total Passing Length (Yards)", y="Total Times Passed (from csv)", title="Total Passing Length vs Total Times Passed")
            graph_div = plotly.offline.plot(fig, output_type="div")
            context['graph_div'] = graph_div

    if request.POST.get('Add') == 'Add':
        form = forms.PassingForm(request.POST)
        if form.is_valid():
            add_player(form)
    
    return render(request,'passing/passing.html', context) 


def parse_form_entries(form):
    global pass_df, players_df
    results = pd.DataFrame()

    # Get values from form
    player_name = form.cleaned_data.get('player_name').title()
    passing_outcome = form.cleaned_data.get('passing_outcome')
    passing_direction = form.cleaned_data.get('passing_direction')
    passing_depth = form.cleaned_data.get('passing_depth')
    passing_length = str(form.cleaned_data.get('passing_length'))

    if player_name:
        player_name = player_name.split()
        first_name = player_name[0]

        if len(player_name) < 2:
            return {'form': form, 'empty': 'Last Name Not Entered!'}

        last_name = player_name[1]
        name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

        if len(name_filter) == 0:
            return {'form': form, 'empty': 'Player Does Not Exist!'}

      
    if passing_outcome != ""  and passing_direction != '' and passing_depth != '' and str(passing_length) != 'None':
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passOutcomes'].values == passing_outcome) & 
                                (pass_df['passLength'].values == passing_length) &
                                (pass_df['passDirection'].values == passing_direction) &
                                (pass_df['passDepth'].values == passing_depth)]

    elif passing_outcome == "" and str(passing_length) != 'None': 
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passLength'].values == passing_length)]

    elif passing_outcome != '': 
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & 
                                (pass_df['passOutcomes'].values == passing_outcome)]

    else:
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

    # If results has data
    if not results.empty:
        results.insert(0, 'Player Name', f'{first_name} {last_name}')
        results = results.drop(columns=_DROP_FRAME)
        results = results.rename(columns=_RENAME_COLS)
        results.insert(loc=0, column='#', value=np.arange(start=1, stop=len(results)+1))


    return {'form': form, 'results': results, 'columns' : results.columns}


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
            'Total Passing Length (Yards)': value[0],
            'Total Times Passed (from csv)': value[1],
            'Average Passing Length (Yards)': value[2],
        }
        temp_df = pd.DataFrame(r_dict, index=[0])
        results = results.append(temp_df, ignore_index=True)

    results.insert(loc=0, column='#', value=np.arange(start=1, stop=len(results)+1))

    return {'analytics': analytics, 'results': results, 'columns' : results.columns, 'n_count' : top_player_count}

# Analytics are done not using Pandas
def top_n_passing_yards(tp_count):
    global pass_df
    total_passing_dict = {}
    pass_dict = pass_df.to_dict()

    for i in range(len(pass_dict['playerId'])):
        cell_val = pass_dict['passLength'][i]
        player_id = pass_dict['playerId'][i]
        if cell_val:
            list_key = [int(cell_val), 1, 0]
            if player_id in total_passing_dict:
                total_passing_dict[player_id][0] += list_key[0]
                total_passing_dict[player_id][1] += list_key[1]
            else:
                total_passing_dict[player_id] = list_key


    passing_yards_desc = sorted(total_passing_dict.items(), key=itemgetter(1), reverse=True)
    # get the top n records from list and cast into a dictionary
    n_records = dict(passing_yards_desc[:tp_count])

    # Calculate average passing yards
    for key, value in n_records.items():
        value[2] = round(value[0]/value[1], 3)

    return n_records


def get_player_name(player_id):
    global players_df
    return players_df.loc[(players_df['playerId'] == player_id)]['nameFull'].values[0]

def add_player(form):
    global pass_df, players_df

    max_pass_id = int(pass_df['passId'].max())
    max_player_id = int(players_df['playerId'].max())

    # Get values from form
    player_name = form.cleaned_data.get('player_name').title()
    passing_outcome = form.cleaned_data.get('passing_outcome')
    passing_direction = form.cleaned_data.get('passing_direction')
    passing_depth = form.cleaned_data.get('passing_depth')
    passing_length = str(form.cleaned_data.get('passing_length'))

    player_name = player_name.split()
    first_name = player_name[0]
    last_name = player_name[1]

    name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

    if len(name_filter) == 0:
        player_id = str(max_player_id+1)
        new_player = pd.DataFrame({'playerId' : player_id, 
                                   'nameFirst' : first_name, 
                                   'nameLast' : last_name, 
                                   'nameFull' : f'{first_name} {last_name}', 
                                   'position': 'QB'
                                   },
                                   index=[0]
                                   )

        players_df = players_df.append(new_player, ignore_index=True)
    else:
        player_id = name_filter['playerId'].values[0]

    if not passing_outcome:
        passing_outcome = 'None'

    if not passing_direction:
        passing_direction = 'None'

    if not passing_depth:
        passing_depth = 'None'

    if not passing_length:
        passing_length = '0'

    new_pass = pd.DataFrame({'passId': str(max_pass_id+1),
                               'playerId': player_id,
                               'passPosition': 'QB',
                               'passOutcomes': passing_outcome,
                               'passDirection': passing_direction,
                               'passDepth': passing_depth,
                               'passLength': passing_length
                               },
                               index=[0]
                               )

    pass_df = pass_df.append(new_pass, ignore_index=True)
