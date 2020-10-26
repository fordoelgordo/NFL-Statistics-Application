from django.shortcuts import get_object_or_404, render

from .nfldata import get_player_dict
from .forms import ReceiveForm, TopReceiveForm


def receiving_page(request):
    submitbutton = request.POST.get("submit")

    player_dict = {}  # store players id and receiving yards
    first_name = ''
    last_name = ''
    form = ReceiveForm(request.POST or None)
    if form.is_valid():

        first_name = form.cleaned_data.get("first_name")  # get first name from form
        last_name = form.cleaned_data.get("last_name")

        # get player dictionary
        player_dict = get_player_dict(first_name, last_name)

        # if dictionary is empty player does not exist in data frame
        # prepare display message indicating so
        if not player_dict:
            first_name = "Does Not Exist"
            last_name = "in data set!!!"

    context = {'form': form, 'first_name': first_name, 'last_name': last_name,
               'player_dict': player_dict, 'submit_button': submitbutton}

    return render(request, 'receiving/receiver.html', context)


def top_receiving_page(request):
    submit_button = request.POST.get("submit")

    form = TopReceiveForm(request.POST or None)

    if form.is_valid():
        player_num = form.cleaned_data.get('player_num')

        print('---------------' + str(player_num) + '---------------')

    context = {'form': form}

    return render(request, 'receiving/topreceiving.html', context)
