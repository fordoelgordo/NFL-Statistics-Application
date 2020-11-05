from django.shortcuts import render
import pandas as pd
from .forms import RushersForm , TeamPickForm
from nfl_site.libraries import readRushers,readTeams,getImageLinks,readPlayers, get_player_dict

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

    #check if name form has been clicked or not
    form = RushersForm(request.POST or None)

    #check if team name form has been clicked or not
    team_form = TeamPickForm(request.POST or None)

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
    
    if team_form.is_valid():
        print('team form has been pressed yessir')
    

    context = {'form': form, 'team_form': team_form,'first_name': first_name, 'last_name':last_name, 'player_dict': player_dict, 
    'submit_button': submitbutton, 'player_team': player_team, 'columns' : outputDataFrame.columns, 'output':outputDataFrame,
    'exists':exists, 'player_img':player_img}
    return render(request, 'rushers/rusher.html', context)




