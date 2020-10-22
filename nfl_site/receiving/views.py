from django.shortcuts import get_object_or_404, render

import pandas as pd
from .forms import ReceiveForm


def recieving_page(request):
    submitbutton = request.POST.get("submit")

    player_dict = {}  # store players id and receiving yards
    player_name = ''

    form = ReceiveForm(request.POST or None)
    if form.is_valid():
        player_dict.clear()  # clear info from previous search

        player_name = form.cleaned_data.get("player_name")  # get player name from form

        split_name = player_name.split()  # split input to get firstname and lastname

        # load player csv from dataset
        df_players \
            = pd.read_csv("static/archive/players.csv")
        # load receiver csv from dataset
        df_receiver \
            = pd.read_csv("static/archive/receiver.csv")

        # filter out players based on the name entered
        name_filter \
            = df_players.loc[(df_players['nameFirst'] == split_name[0]) & (df_players['nameLast'] == split_name[1])]

        if len(name_filter) == 0:
            # if player does not exist set tuple to false and empty string
            temp_tup = False, []
        else:
            # if player does exist return list of id's of all players with the same name
            player_id_list = name_filter['playerId'].tolist()
            temp_tup = True, player_id_list

        if not temp_tup[0]:
            # if first value in the tuple is false the name entered does nott exist in data set
            player_name = 'Does not exist in data set'
            player_dict = []
        else:

            # for each player id in the player id list (the second value in temp tup) find all occuences of the player
            # id in the receiver csv
            for player_id in temp_tup[1]:

                # get all receiving plays for a player based on id if play was a reception,
                # pass was not intercepted, and reception was not overturned
                receiving_filter \
                    = df_receiver.loc[(df_receiver['playerId'] == player_id) & (df_receiver['rec'] == 1)
                                      & (df_receiver['recPassInt'] == 0) & (df_receiver['recNull'] == 0)]

                # Note players are added to a python dictionary with id as key and value bwing the total receiving yards
                # i.e. player_dict[player_id] = Total receiving yards
                if len(receiving_filter) == 0:
                    # if no results found player has zero receiving yards
                    player_dict[player_id] = 0
                else:
                    # sum the recYards row of the data frame
                    total_rec_yards = receiving_filter['recYards'].sum()

                    player_dict[player_id] = int(total_rec_yards)

                # print(player_dict)

    context = {'form': form, 'player_name': player_name, 'player_dict': player_dict, 'submit_button': submitbutton}

    return render(request, 'receiving/receiver.html', context)
