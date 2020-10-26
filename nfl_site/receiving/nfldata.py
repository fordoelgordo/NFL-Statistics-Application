import pandas as pd
import pathlib

if pathlib.Path('static/archive/').exists():
    # load player csv from dataset
    df_players = pd.read_csv("static/archive/players.csv")
    # load receiver csv from dataset
    df_receiver = pd.read_csv("static/archive/receiver.csv")


def get_player_id(firstname, lastname):
    name_filter = df_players.loc[(df_players['nameFirst'] == firstname) & (df_players['nameLast'] == lastname)]

    if len(name_filter) == 0:
        # if player does not exist set tuple to false and empty string
        return False, []
    else:
        # if player does exist return list of id's of all players with the same name
        player_id = name_filter['playerId'].tolist()
        return True, player_id


def get_receiving_yards(player_id):
    # get all receiving plays for a player based on id if play was a reception,
    # pass was not intercepted, and reception was not overturned
    receiving_filter \
        = df_receiver.loc[(df_receiver['playerId'] == player_id) & (df_receiver['rec'] == 1)
                          & (df_receiver['recPassInt'] == 0) & (df_receiver['recNull'] == 0)]

    if len(receiving_filter) == 0:
        # return zero if player has no receiving yards
        return 0
    else:
        # return sum if player has receiving yards
        total_rec_yards = receiving_filter['recYards'].sum()
        return total_rec_yards


def get_player_dict(firstname, lastname):

    player_tuple = get_player_id(firstname, lastname)

    if not player_tuple[0]:
        # if first value in the tuple is false the name entered does not exist in data set
        # return empty dict
        return {}
    else:
        temp_dict = {}

        # if name(s) do exist loop through all in list and add them to dictionary that is then returned
        for player_id in player_tuple[1]:

            total_yards = get_receiving_yards(player_id)
            temp_dict[player_id] = total_yards

        return temp_dict
