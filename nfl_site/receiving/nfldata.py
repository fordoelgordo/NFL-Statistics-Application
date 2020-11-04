import pathlib



from operator import itemgetter
from nfl_site.libraries import csv_to_dict

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

            # create key to get rec plays from prp dictionary
            tup_key = (pid, firstname + ' ' + lastname)

            if tup_key in prp.keys():

                temp_dict[pid] = (total_yards, float(total_yards)/float(prp[tup_key]), prp[tup_key])
            else:
                temp_dict[pid] = (total_yards, 0.0, 0)

        return temp_dict


def top_n_rec_yards(num):

    pid_list = receiver_dict['playerId']
    total_rec_dict = {}
    total_avg_rec_dict = {}

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

    # create dictionary containing keys (player id, player name)
    # and values (receiving yards, avg receiving yards per play, and total plays)
    for key, val in n_records.items():
        if key in prp.keys():
            total_avg_rec_dict[key] = (val, float(val) / float(prp[key]), prp[key])
        else:
            total_avg_rec_dict[key] = (val, 0.0, 0.0)

    return total_avg_rec_dict


# get total receiving plays for players in receiver.csv
def player_rec_plays():
    pid_list = receiver_dict['playerId']
    rec_plays_dict = {}

    for i in range(len(pid_list)):

        if pid_list[i] in player_id_name_lookup.keys():
            tup_key = (pid_list[i], player_id_name_lookup[pid_list[i]])
            # if tuple key containing player id and full name does not exist in dictionary create a new
            # entry else add to the rec plays
            if tup_key not in rec_plays_dict:
                rec_plays_dict[tup_key] = 1
            else:
                rec_plays_dict[tup_key] += 1

    return rec_plays_dict


if pathlib.Path('static/archive/').exists():

    player_dict = csv_to_dict("static/archive/players.csv")
    receiver_dict = csv_to_dict("static/archive/receiver.csv")
    player_id_name_lookup = create_id_name_lookup()  # dictionary that can get player name given id
    prp = player_rec_plays()  # get dictionary containing players and their total receiving plays
