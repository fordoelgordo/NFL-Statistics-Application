from django.shortcuts import get_object_or_404, render

from .nfldata import get_player_dict, top_n_players
from .forms import ReceiveForm, TopReceiveForm


def receiving_page(request):
    submitbutton = request.POST.get("submit")

    player_dict = {}  # store players id and receiving yards
    first_name = ''
    last_name = ''
    full_name = ''
    error_message = ''
    column_names = ['Player ID', 'Full Name', 'Total Receiving Yards']

    form = ReceiveForm(request.POST or None)
    if form.is_valid():

        first_name = form.cleaned_data.get("first_name")  # get first name from form
        last_name = form.cleaned_data.get("last_name")
        full_name = first_name + " " + last_name
        # get player dictionary
        player_dict = get_player_dict(first_name, last_name)

        # if dictionary is empty player does not exist in data frame
        # prepare display message indicating so
        if not player_dict:
            error_message = "Error: Does Not Exist in data set!!!"

    context = {'form': form, 'full_name': full_name, 'error_msg': error_message,
               'column_names': column_names, 'player_dict': player_dict, 'submit_button': submitbutton}

    return render(request, 'receiving/receiver.html', context)


def top_receiving_page(request):
    submit_button = request.POST.get("submit")

    form = TopReceiveForm(request.POST or None)

    top_player_dict = {}
    column_names = ['Player ID', 'Full Name', 'Total Receiving Yards']

    if form.is_valid():
        player_num = form.cleaned_data.get('player_num')

        # get dictionary containing top players
        top_player_dict = top_n_players(player_num)

    context = {'form': form, 'column_names': column_names,
               'top_player_dict': top_player_dict, 'submit_button': submit_button}

    return render(request, 'receiving/topreceiving.html', context)
