import pathlib


from static.team42libraries.csvtodict import csv_to_dict
from operator import itemgetter


# create Dictionary to quickly look up player names
def create_id_name_lookup():
    pid_list = player_dict['playerId']

    lookup_dict = {}

    for i in range(len(pid_list)):
        lookup_dict[pid_list[i]] = player_dict['nameFull'][i]

    return lookup_dict


def get_player_id(firstname, lastname):
    # get columns of values
    list1 = player_dict['nameFirst']
    list2 = player_dict['nameLast']

    id_list = []  # list to hold player ids

    fullname = firstname + ' ' + lastname

    # if column length is not the same there is a problem with data
    if len(list1) == len(list1):
        # iterate through first and last name columns
        for i in range(len(list2)):
            list_name = list1[i] + ' ' + list2[i]
            # if name is found add id to list
            if fullname == list_name:
                player_id = player_dict['playerId'][i]
                id_list.append(player_id)

        # return list of ids
        return id_list
    else:
        print('Error: Mismatched column length')
        return None


def get_receiving_yards(player_id):
    pid_list = receiver_dict['playerId']
    total_rec_yards = 0

    for i in range(len(pid_list)):
        if pid_list[i] == player_id:
            if receiver_dict['rec'][i] == '1' and receiver_dict['recPassInt'][i] == '0' \
                    and receiver_dict['recNull'][i] == '0':
                cell_val = receiver_dict['recYards'][i]  # get value contained in cell of recYards column
                # check to make sure cell does not contain the None data type to prevent addition errors
                if cell_val:
                    total_rec_yards += int(cell_val)

    return total_rec_yards


def get_rec_yards_dict(firstname, lastname):
    player_ids = get_player_id(firstname, lastname)  # this is a list of player ids that match name

    if not player_ids:
        # if list returned by get_player_id is empty name does not exist in dataset
        # return empty dictionary
        return {}
    else:
        temp_dict = {}
        # if list returned by get_player_id is not empty get total rec yards for each id
        for pid in player_ids:
            total_yards = get_receiving_yards(pid)
            temp_dict[pid] = total_yards

        return temp_dict


def top_n_rec_yards(num):

    pid_list = receiver_dict['playerId']
    total_rec_dict = {}

    for i in range(len(pid_list)):
        if receiver_dict['rec'][i] == '1' and receiver_dict['recPassInt'][i] == '0' \
                and receiver_dict['recNull'][i] == '0':
            cell_val = receiver_dict['recYards'][i]  # get value contained in cell of recYards column
            # check to make sure cell does not contain the None data type to prevent addition errors
            if cell_val:
                # create key for dictionary which is a tuple containing player id and full name
                tup_key = (pid_list[i], player_id_name_lookup[pid_list[i]])
                # if tuple key containing player id and full name does not exisis in dictionary create a new
                # entry else add to the total rec yards
                if tup_key not in total_rec_dict:
                    total_rec_dict[tup_key] = int(cell_val)
                else:
                    total_rec_dict[tup_key] += int(cell_val)

    # sort dictionary by total rec yards in descending order
    # Note: this returns a list not a dictionary
    rec_yards_desc = sorted(total_rec_dict.items(), key=itemgetter(1), reverse=True)
    # get the top n records from list and cast into a dictionary
    n_records = dict(rec_yards_desc[:num])

    return n_records


if pathlib.Path('static/archive/').exists():

    player_dict = csv_to_dict("static/archive/players.csv")
    receiver_dict = csv_to_dict("static/archive/receiver.csv")
    player_id_name_lookup = create_id_name_lookup()
