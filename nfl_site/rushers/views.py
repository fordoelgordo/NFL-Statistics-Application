from django.shortcuts import render
import pandas as pd
from .forms import RushersForm

#for getting image from .html
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re



# Create your views here.

def rusher_page(request):
    submitbutton = request.POST.get("submit")
    # store players id and rushing yards
    player_dict = {}  
    first_name = ''
    last_name = ''
    player_team = []
    outputDataFrame = pd.DataFrame()
    exists = None
    player_img = ''

    # load players csv from dataset
    df_players = readPlayers()

    # load rushers csv from dataset
    df_rusher = readRushers()

    #load teams csv from dataset
    df_teams = readTeams()

    #check if form has been clicked or not
    form = RushersForm(request.POST or None)

    if form.is_valid():
        player_dict.clear()  # clear info from previous search
        first_name = form.cleaned_data.get("first_name")  # get player first name from form
        last_name = form.cleaned_data.get("last_name") # get player last name from form
        # filter out players based on the name entered
        outputDataFrame = get_player_dict(df_players,first_name,last_name,df_rusher)

        # if dictionary is empty player does not exist in data frame
        # prepare display message indicating so
        if outputDataFrame.empty:
            first_name = "Player Does Not Exist"
            last_name = "In Data Set!"
            exists = 0
        else:
            player_img =  getImageLinks(first_name,last_name)

    context = {'form': form, 'first_name': first_name, 'last_name':last_name, 'player_dict': player_dict, 
    'submit_button': submitbutton, 'player_team': player_team, 'columns' : outputDataFrame.columns, 'output':outputDataFrame,
    'exists':exists, 'player_img':player_img}
    return render(request, 'rushers/rusher.html', context)


def readPlayers():
    return pd.read_csv("static/archive/players.csv")

def readRushers():
    return pd.read_csv("static/archive/rusher.csv")


def get_Tuple(df_players,first_name,last_name):
    name_filter = df_players.loc[(df_players['nameFirst'] == first_name) & (df_players['nameLast'] == last_name)]
    if len(name_filter) == 0:
        # if player does not exist set tuple to false and empty string
        return False, []
    else:
        # if player does exist return list of id's of all players with the same name
        player_id_list = name_filter['playerId'].tolist()
        return True, player_id_list

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
    return team_names

def get_player_dict(df_players, first_name, last_name, df_rusher):
    player_dict = {} 
    outputDataFrame = pd.DataFrame() 
    player_tuple = get_Tuple(df_players,first_name, last_name)

    if not player_tuple[0]:
        # if first value in the tuple is false the name entered does not exist in data set
        # return empty dict
        return outputDataFrame
    else:
        # for each player id in the player id list (the second value in temp tup) find all occuences of the player
        # id in the receiver csv
        for player_id in player_tuple[1]:
            print(player_id)
            # get all rusher yards for playerId as long as they exist and were not overturned
            rushers_filter \
                = df_rusher.loc[(df_rusher['playerId'] == player_id) & (df_rusher['rushNull'] == 0)]
            # sum the rushYards row of the data frame
            total_rush_yards = rushers_filter['rushYards'].sum()

            player_dict[player_id] = int(total_rush_yards)
            player_team_id = getPlayerTeam(player_id)
            player_team = getTeamName(player_team_id)
            print(player_team)
            outputDataFrame = outputDataFrame.append([[first_name,last_name,player_id,player_dict[player_id],player_team]])
        
        outputDataFrame.columns = ['First Name', 'Last Name', 'Player ID','Rush Yards','Team(s)']
        return outputDataFrame

def getImageLinks(first_name,last_name):
    site ='https://www.nfl.com/players/'+str(first_name)+'-'+str(last_name)+'/'
    substr = 'https://static.www.nfl.com/image/private/t_player_profile_landscape/'
    html = urlopen(site)
    bs = BeautifulSoup(html, 'html.parser')
    full_name = str(first_name)+' '+str(last_name)
    images = bs.find_all('img', {"alt": full_name })
    pathToImage = ''
    for image in images:
        url = image['src']
        if substr in url:
            pathToImage = url.replace('t_lazy/','')
            print(pathToImage)
    return pathToImage



