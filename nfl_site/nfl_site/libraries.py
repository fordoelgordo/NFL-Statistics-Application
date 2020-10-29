'''
Author: FSt. J
Comments: We'll use this .py file to maintain all of our user-defined functions for the project
          Note that functions within this code can be called using the following syntax
          from nfl_site.nfl_site.libraries import <my_function1>, <my_function2>, ... : for specific functions OR
          from nfl_site.nfl_site.libraries import * : for all functions
'''

'''
Author: FSt.J
Comments: Global function to convert  heigh in decimal inches to cleaner view
'''
import pandas as pd
#for getting image from .html
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def conv_height(h):
    ft = int(divmod(h,12)[0])
    inch = round(int(divmod(h,12)[1]),0)
    if h == 0 or h == "" or h == " ":
        return ""
    else:
        return str(ft)+"'"+str(inch)+"\""

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



# ================== Below are functions that are used by the Rushers site ==================
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

# ================== Above are functions that are used by the Rushers site ==================
