from django.shortcuts import render
import pandas as pd
import pathlib
import numpy as np
from standings import forms
from nfl_site.libraries import csv_to_dict

# Create your views here.
'''
Author: FSt.J
Code Comments: return NFL win-loss statistics to the user
'''
# NFL Data relative path
data_path = 'static/archive/'

# Check if the csv path exists
draft = ""
teams = ""
games = ""
combined = ""
if pathlib.Path(data_path).exists():
    # Get team name and team ID to join to gameplay stats dataset
    draft = pd.read_csv(data_path + 'draft.csv')
    teams = draft[['draft','draftTeam','teamId']]
    teams = teams.drop_duplicates()
    teams = teams[teams['draft'] >= 2004]
    teams = teams.sort_values(['teamId','draft'], ascending = [True,True])

    # Drop teamId that map to mulitple teams for the same year
    indexes = teams[(teams['draft'] == 2019) & (teams['draftTeam'] == 'HOU') & (teams['teamId'] == 2100)].index # Remove this Houston record
    teams.drop(indexes, inplace=True)
    indexes = teams[(teams['draft'] < 2019) & (teams['draftTeam'] == 'LAC')].index # Remove LAC records prior to 2019
    teams.drop(indexes, inplace=True)
    indexes = teams[(teams['draft'] == 2019) & (teams['draftTeam'] == 'LAR') & (teams['teamId'] == 2520)].index # Remove LAC records prior to 2019
    teams.drop(indexes, inplace=True)
    teams.loc[teams['teamId'] == 3800, 'draftTeam'] = 'ARI'
    teams.loc[teams['teamId'] == 325, 'draftTeam'] = 'BAL'
    teams.loc[teams['teamId'] == 1050, 'draftTeam'] = 'CLE'

    # Read in games data
    games = pd.read_csv(data_path + 'games.csv')
    games.drop(['homeTeamDistance','visitingTeamDistance'], axis=1, inplace=True)
    
    # Merge the datasets to append the team names
    games_m = pd.merge(games, teams, how='inner',left_on=['homeTeamId','season'],right_on=['teamId','draft'])
    games_m = games_m.drop(['teamId','homeTeamId','draft'], axis=1)
    games_m = games_m.rename(columns={'draftTeam':'homeTeam'})
    games_m = pd.merge(games_m, teams, how='inner',left_on=['visitorTeamId','season'],right_on=['teamId','draft'])
    games_m = games_m.drop(['teamId','visitorTeamId','draft'], axis=1)
    games_m = games_m.rename(columns={'draftTeam':'visitorTeam'})
    games_m = pd.merge(games_m, teams, how='inner',left_on=['winningTeam','season'],right_on=['teamId','draft'])
    games_m = games_m.drop(['teamId','winningTeam','draft'], axis=1)
    games_m = games_m.rename(columns={'draftTeam':'winningTeam'})
    
    # Compute win/loss, along with total points scored
    games_m['homeWin'] = np.where(games_m['homeTeam'] == games_m['winningTeam'], 1, 0)
    games_m['visitWin'] = np.where(games_m['visitorTeam'] == games_m['winningTeam'], 1, 0)

# Now aggregate the data
home_agg = games_m.groupby(
    ['season','homeTeam','seasonType'], as_index = False
).agg(
    {
        'homeTeamFinalScore':sum, # Sum home-team points
        'visitingTeamFinalScore':sum, # Sum visting-team points
        'homeWin': sum,
        'visitWin':sum
    }
)
home_agg.columns = list(map(''.join, home_agg.columns.values))
visit_agg = games_m.groupby(
    ['season','visitorTeam','seasonType'], as_index = False
).agg(
    {
        'homeTeamFinalScore': sum,
        'visitingTeamFinalScore': sum,
        'homeWin': sum,
        'visitWin': sum
    }
)
visit_agg.columns = list(map(''.join, visit_agg.columns.values))
combined = pd.merge(home_agg, visit_agg, how='inner',left_on=['season','homeTeam','seasonType'], right_on=['season','visitorTeam','seasonType'])
combined = combined.rename(columns={'homeTeam':'NFL Team'})

#Aggregate the correct columns now to get the correct records
combined['PF'] = combined.apply(lambda x: int(x['homeTeamFinalScore_x'] + x['visitingTeamFinalScore_y']), axis=1)
combined['PA'] = combined.apply(lambda x: int(x['visitingTeamFinalScore_x'] + x['homeTeamFinalScore_y']), axis=1)
combined['Wins'] = combined.apply(lambda x: int(x['homeWin_x'] + x['visitWin_y']), axis = 1)
combined['Losses'] = combined.apply(lambda x: int(x['visitWin_x'] + x['homeWin_y']), axis = 1)
combined['WinPct'] = combined.apply(lambda x: "%0.2f%%" % (100 * x['Wins'] / (x['Wins'] + x['Losses'])), axis = 1)
combined['Net Pts'] = combined.apply(lambda x: int(x['PF'] - x['PA']), axis = 1)
combined.drop(['homeTeamFinalScore_x','visitingTeamFinalScore_x','homeWin_x','visitWin_x','visitorTeam','homeTeamFinalScore_y','visitingTeamFinalScore_y','homeWin_y','visitWin_y'], axis=1, inplace=True)

# Append the division and conference to the dataset
combined['Conference'] = np.where(combined['NFL Team'].isin(['NO','GB','SEA','LAR','TB','ARI','CHI','SF','DET','MIN','CAR','PHI','ATL','WAS','DAL','NYG']), 'NFC','AFC')
def set_div(x):
    if x['NFL Team'] in ['LAR','SEA','ARI','SF','KC','LV','DEN','LAC']:
        return 'West'
    if x['NFL Team'] in ['NO','TB','CAR','ATL','IND','TEN','HOU','JAX']:
        return 'South'
    if x['NFL Team'] in ['PHI','NYG','DAL','WAS','BUF','MIA','NE','NYJ']:
        return 'East'
    if x['NFL Team'] in ['GB','CHI','MIN','DET','PIT','CLE','CIN','BAL']:
        return 'North'
combined['Division'] = combined.apply(set_div, axis=1)

# Re-arrange the ordering of the columns
combined = combined[['NFL Team','Conference','Division','season','seasonType','Wins','Losses','WinPct','PF','PA','Net Pts']]

# response/combine page rendering
def standings(request):
    year_form = forms.YearForm
    
    # Set holding variables
    year_val = 0
    season_val = ""
    combined_filtered = combined
    league = False
    df_dict = []
    df_rec = []

    if request.method == "POST": # Means someone filled out our player_form
        year_form = forms.YearForm(request.POST)
        if year_form.is_valid():
            year_val = year_form.cleaned_data.get('year_val')
            season_val = year_form.cleaned_data.get('season_val')
            if year_val:
                combined_filtered = combined_filtered[combined_filtered['season'] == year_val]
                combined_filtered.drop('season', axis=1, inplace=True)
            if season_val:
                combined_filtered = combined_filtered[combined_filtered['seasonType'] == season_val]
                combined_filtered.drop('seasonType', axis=1, inplace=True)
            # Sort by winning percentage
            combined_filtered.sort_values(by=['WinPct','Wins','PF','PA'], ascending =[False,False,False,True], inplace = True, na_position='first')

    if request.POST.get('Division') == 'Division':
        print("Division button clicked")

    if request.POST.get('Conference') == 'Conference':
        print("Conference button clicked")

    if request.POST.get('League') == 'League':
        league = True
        df_dict = combined_filtered.to_dict()
        df_rec = combined_filtered.to_dict(orient='records')
           
    context = {'year_form': year_form, 'df_dict':df_dict, 'df_rec':df_rec, 'league':league}
    return render(request, 'standings/standings.html', context)