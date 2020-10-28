from django.shortcuts import render
import pandas as pd
from .forms import RushersForm


# Create your views here.

def rusher_page(request):
    submitbutton = request.POST.get("submit")
    # store players id and rushing yards
    player_dict = {}  
    first_name = ''
    last_name = ''
    player_team = []

    #check if form has been clicked or not
    form = RushersForm(request.POST or None)

    if form.is_valid():
        player_dict.clear()  # clear info from previous search
        first_name = form.cleaned_data.get("first_name")  # get player first name from form
        last_name = form.cleaned_data.get("last_name") # get player last name from form
        #split_name = player_name.split()  # split input to get firstname and lastname

        # load players csv from dataset
        df_players = readPlayers()

        # load rushers csv from dataset
        df_rusher = readRushers()

        #load teams csv from dataset
        df_teams = readTeams()

        # filter out players based on the name entered
        name_filter = readPlayerName(df_players,first_name,last_name)
        
        if len(name_filter) == 0:
            # if player does not exist set tuple to false and empty string
            temp_tup = False, []
        else:
            # if player does exist return list of id's of all players with the same name
            player_id_list = name_filter['playerId'].tolist()
            temp_tup = True, player_id_list

        if not temp_tup[0]:
            # if first value in the tuple is false the name entered does nott exist in data set
            first_name = 'Does not exist'
            last_name = ' in data set!'
            player_dict = []
        else:

            # for each player id in the player id list (the second value in temp tup) find all occuences of the player
            # id in the receiver csv
            for player_id in temp_tup[1]:

                # get all rusher yards for playerId as long as they exist and were not overturned
                rushers_filter \
                    = df_rusher.loc[(df_rusher['playerId'] == player_id) & (df_rusher['rushNull'] == 0)]


                # Note players are added to a python dictionary with id as key and value bwing the total rusher yards
                # i.e. player_dict[player_id] = Total rushing yards
                if len(rushers_filter) == 0:
                    # if no results found player has zero receiving yards
                    player_dict[player_id] = 0
                else:
                    # sum the rushYards row of the data frame
                    total_rush_yards = rushers_filter['rushYards'].sum()

                    player_dict[player_id] = int(total_rush_yards)
                    player_team_id = getPlayerTeam(player_id)
                    player_team = getTeamName(player_team_id)
                    # print(player_dict)


    context = {'form': form, 'first_name': first_name, 'last_name':last_name, 'player_dict': player_dict, 'submit_button': submitbutton, 'player_team': player_team}

    return render(request, 'rushers/rusher.html', context)


def readPlayers():
    return pd.read_csv("static/archive/players.csv")

def readRushers():
    return pd.read_csv("static/archive/rusher.csv")


def readPlayerName(df_players,first_name,last_name):
    return df_players.loc[(df_players['nameFirst'] == first_name) & (df_players['nameLast'] == last_name)]

def readTeams():
    df = pd.read_csv("static/archive/draft.csv")
    team_df = df[['teamId','draftTeam']].drop_duplicates()
    return team_df

def getPlayerTeam(player_id):
    df = readRushers()
    filter_df = df.loc[(df['playerId'] == player_id)]
    get_team = filter_df['teamId'].drop_duplicates().tolist()
    return get_team

def getTeamName(team_id):
    df = readTeams()
    team_names = []
    for i in team_id:
        team_name = df[df['teamId'] == i]['draftTeam'].unique().tolist()
        team_names.append(team_name)
    print(team_names)
    return team_names
