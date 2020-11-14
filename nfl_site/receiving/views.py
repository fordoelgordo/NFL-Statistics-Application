from django.shortcuts import get_object_or_404, render

from .nfldata import get_rec_yards_dict, top_n_rec_yards, avg_rec_yard_scatter, add_receiver_data, add_existing_receiver_data
from .forms import ReceiveForm, TopReceiveForm, AddReceivingPlayForm

# player_dict: key is players id. value is the following
# array [player name, total receiving yards. avg rec yards per play, total receiving plays]
player_dict = {}


def receiving_page(request):

    global player_dict
    button_click = ''
    error_message = ''
    player_dict_loaded = ''
    column_names = ['Player ID', 'Full Name', 'Total Receiving Yards',
                    'Avg. Rec. Yards per Rec. Play', 'Total Receiving Plays']

    # if player_dict still contains data set flag to show it when user returns to receiving statistics page
    if player_dict:
        player_dict_loaded = 'true'

    form = ReceiveForm(request.POST or None)
    add_rec_play_form = AddReceivingPlayForm(request.POST or None)

    if request.POST.get('Search') == 'Search':
        if form.is_valid():
            button_click = 'Clicked'

            first_name = form.cleaned_data.get("first_name")  # get first name from form
            last_name = form.cleaned_data.get("last_name")

            # get player dictionary containing receiving yards info
            player_dict = get_rec_yards_dict(first_name, last_name)

            # if dictionary is empty player does not exist in data frame
            # prepare display message indicating so
            if not player_dict:
                error_message = "Error: Does Not Exist in data set!!!"

    if request.POST.get('Add') == 'Add':
        if add_rec_play_form.is_valid():
            button_click = 'Clicked'

            player_id = add_rec_play_form.cleaned_data.get('player_id')
            rec_yards = add_rec_play_form.cleaned_data.get('rec_yards')
            position = add_rec_play_form.cleaned_data.get('rec_position')

            if player_dict and player_id in player_dict.keys():
                # update the current values displayed in the table, so that the entire avg receiving yards per play
                # calculation does not need to be computed again
                update_existing_player_dict(player_id, rec_yards, position)
            else:

                data_add = add_existing_receiver_data(player_id, position, str(rec_yards))

                if not data_add:
                    error_message = "Receiving data could not be added. Player with ID: " \
                                    + player_id + " does not exist."
                else:
                    # this not an error it is message that receiving data was added
                    error_message = "receiving data successfully added for player with Id: " + player_id

    context = {'form': form, 'add_rec_play_form': add_rec_play_form, 'error_msg': error_message,
               'column_names': column_names, 'player_dict': player_dict,
               'player_dict_loaded' : player_dict_loaded, 'button_click': button_click}

    return render(request, 'receiving/receiver.html', context)


def top_receiving_page(request):
    submit_button = request.POST.get("submit")

    form = TopReceiveForm(request.POST or None)
    top_player_dict = {}
    graph_div = ''
    column_names = ['Player ID', 'Full Name', 'Total Receiving Yards',
                    'Avg. Rec. Yards per Rec. Play', 'Total Receiving Plays']

    if form.is_valid():
        player_num = form.cleaned_data.get('player_num')

        # get dictionary containing top players
        top_player_dict = top_n_rec_yards(player_num)

        if top_player_dict:
            graph_div = avg_rec_yard_scatter(top_player_dict)

    context = {'form': form, 'column_names': column_names, 'graph_div': graph_div,
               'top_player_dict': top_player_dict, 'submit_button': submit_button}

    return render(request, 'receiving/topreceiving.html', context)


# update data for a player that is currently being displayed to the user
def update_existing_player_dict(player_id, rec_yards, position):
    global player_dict

    if player_id in player_dict.keys():
        # recalculate the total receiving yards
        player_dict[player_id][1] = str(int(player_dict[player_id][1]) + rec_yards)
        # increment the total receiving plays
        player_dict[player_id][3] = str(int(player_dict[player_id][3]) + 1)
        # recalculate the avg receiving yards per play
        player_dict[player_id][2] = str(float(player_dict[player_id][1])/float(player_dict[player_id][3]))

        # add the receiving play to the receiver data store so it can persist while site is running
        add_receiver_data(player_id, position, str(rec_yards))
