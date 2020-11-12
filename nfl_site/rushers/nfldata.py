import pandas as pd
#for getting image from .html
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pathlib
import datetime



# ================== Below are functions that are used by the Rushers site ==================

def readPlayers():
    return pd.read_csv("static/archive/players.csv")

def readRushers():
    return pd.read_csv("static/archive/rusher.csv")

def readTeams():
    df = pd.read_csv("static/archive/draft.csv")
    team_df = df[['teamId','draftTeam']].drop_duplicates()
    return team_df

if pathlib.Path('static/archive/').exists():
    df_rusher = readRushers()
    df_teams = readTeams()
    df_players = readPlayers()
    all_rushers = df_rusher[["playerId","rushYards","rushNull"]]



# dataTeam = 'https://gist.githubusercontent.com/cnizzardini/13d0a072adb35a0d5817/raw/dbda01dcd8c86101e68cbc9fbe05e0aa6ca0305b/nfl_teams.csv'
# team_df = pd.read_csv(dataTeam,error_bad_lines=False)
# print(team_df)

# For getting the record number or index of a certain record in a data frame
# params: ( dataframe, value of row to take out) e.g: (players, playerID)
def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

def get_Tuple(df_players,first_name,last_name):
    name_filter = df_players.loc[(df_players['nameFirst'] == first_name) & (df_players['nameLast'] == last_name)]
    if len(name_filter) == 0:
        # if player does not exist set tuple to false and empty string
        return False, []
    else:
        # if player does exist return list of id's of all players with the same name
        player_id_list = name_filter['playerId'].tolist()
        return True, player_id_list



def getPlayerTeam(player_id):
    filter_df = df_rusher.loc[(df_rusher['playerId'] == player_id)]
    get_team = filter_df['teamId'].drop_duplicates().tolist()
    return get_team

def getTeamName(team_id):
    team_names = []
    for i in team_id:
        team_name = df_teams[df_teams['teamId'] == i]['draftTeam'].unique().tolist()
        team_names.append(team_name)
    return team_names

# def get_all_teams_dic():
#     all_teams = df_teams[['teamId']['draftTeam']].unique().tolist()
#     print(all_teams)

def get_total_yards_for_player(player_id):
    player_rush_yards = int(all_rushers.loc[(all_rushers['playerId'] == player_id,'rushYards')].sum())
    return player_rush_yards

def get_player_df(first_name, last_name):
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
            # get all rusher yards for playerId as long as they exist
            player_dict[player_id] = get_total_yards_for_player(player_id)
            player_team_id = getPlayerTeam(player_id) #list of teams player 
            player_team = getTeamName(player_team_id) 
            print(player_team)
            outputDataFrame = outputDataFrame.append([[first_name,last_name,player_id,player_dict[player_id],player_team]])
        
        outputDataFrame.columns = ['First Name', 'Last Name', 'Player ID','Rush Yards','Team(s)']
        return outputDataFrame


# function to get a rushers yards in the dictionary 
def get_rushers_yards(dic , rusher_id):
    for key,value in dic.items():
        if key == rusher_id:
            return value

def get_name(player_id):
    player_df = df_players.loc[(df_players['playerId'] == player_id)].drop_duplicates()
    first_name = player_df["nameFirst"].values
    last_name = player_df["nameLast"].values
    # we use first_name[0] becuase the name is "['Tom'] "", this makes it just "Tom"
    # i think this is due it being an array 
    full_name = [first_name[0],last_name[0]]
    return full_name

# function to get rushers dictionary {player id} = {total yards they have}
def get_rusher_yards_dic():
    total_rusher_dic = {}
    player_id = all_rushers[["playerId"]].drop_duplicates().values.tolist()


    #TODO: Less Expensive, figure out how to reduce costs of lookup or move into own function
    a = datetime.datetime.now()
    for id in player_id:
        # total_yards = all_rushers.loc[(all_rushers['playerId'] == id[0],'rushYards')].sum()
        total_yards = get_total_yards_for_player(id[0])
        total_rusher_dic.update({id[0]:total_yards})
    b = datetime.datetime.now()
    c = b - a
    # print(c)
    return total_rusher_dic


def get_total_plays(id):
   play_count = all_rushers.loc[(all_rushers['playerId'] == id)].count() 
   total_plays_for_player = int(play_count['playerId'])
   return total_plays_for_player


# creating the output dataframe of top rushers
def get_top_rushers_df(top_rushers):
    outputDataFrame = pd.DataFrame()
    rank = 0

    for id in top_rushers:
        full_name = get_name(id)
        first_name = full_name[0]
        last_name = full_name[1]
        rusher_total_yds = int(get_rushers_yards(top_rushers,id))
        rusher_total_plays = get_total_plays(id)
        rusher_avg_yds = round(rusher_total_yds/rusher_total_plays,3)
        player_team_id = getPlayerTeam(id)
        player_team = getTeamName(player_team_id) 
        rank = rank + 1
        outputDataFrame = outputDataFrame.append([[rank,first_name,last_name,id,rusher_total_yds,rusher_avg_yds,rusher_total_plays,player_team]])
    
    outputDataFrame.columns = ['Rank','First Name', 'Last Name', 'Player ID','Rush Yards','Avg Yards(per play)','Total Plays','Team(s)']
    return outputDataFrame

# create context for Top Rushers
def create_ALL_TIME_context(form,team_form,team_submit,show_graph_button,outputDataFrame,exists):
    context = {'form': form, 'team_form': team_form,'team_submit': team_submit,'show_graph_button':show_graph_button,'columns' : outputDataFrame.columns, 'output':outputDataFrame,
    'exists':exists}
    return context


# get path to image for player 
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

# ================== Above are functions that are used by the Rushers site =================