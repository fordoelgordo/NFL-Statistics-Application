from django.shortcuts import render
import pandas as pd
from .forms import RushersForm , TeamPickForm
from .nfldata import get_player_dict,get_rusher_yards_dic,get_top_rushers_df,create_ALL_TIME_context, getImageLinks


def rusher_page(request):
    
    # store players id and rushing yards
    player_dict = {}  
    context = {}
    first_name = ''
    last_name = ''
    player_team = []
    outputDataFrame = pd.DataFrame()
    exists = None
    player_img = ''

    team_img = ''
    team_name = ''

    submitbutton = request.POST.get("Search")
    team_submit = request.POST.get("Team Picker")

    #check if name form has been clicked or not
    form = RushersForm()
    #check if team name form has been clicked or not
    team_form = TeamPickForm()

    if(submitbutton == 'Search'):
        form = RushersForm(request.POST)
        if form.is_valid():
            player_dict.clear()  # clear info from previous search
            first_name = form.cleaned_data.get("first_name")  # get player first name from form
            last_name = form.cleaned_data.get("last_name") # get player last name from form
            # filter out players based on the name entered
            outputDataFrame = get_player_dict(first_name,last_name)

            # if dictionary is empty player does not exist in data frame
            # prepare display message indicating so
            if outputDataFrame.empty:
                first_name = "Player Does Not Exist"
                last_name = "In Data Set!"
                exists = 0
            else:
                player_img =  getImageLinks(first_name,last_name)
            context = {'form': form, 'team_form':team_form, 'first_name': first_name, 'last_name':last_name, 
            'submit_button': submitbutton,  'columns' : outputDataFrame.columns, 'output':outputDataFrame,
            'exists':exists, 'player_img':player_img}       
    
    if (team_submit == 'Team Picker'):
        team_form = TeamPickForm(request.POST)
        if team_form.is_valid():
            #dictionary of player id to their yards
            rusher_dic = get_rusher_yards_dic() 
            
            #getting the top 20 rushers [player id] = [total rush yards] 
            #Reverse ordered because we want top players first
            top_rushers = dict(sorted(rusher_dic.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)[:20])
            outputDataFrame = get_top_rushers_df(top_rushers)
            exists = 1
            context = create_ALL_TIME_context(form,team_form,team_submit,outputDataFrame,exists)

    if not context:
        context = {'form': form, 'team_form': team_form}

    return render(request, 'rushers/rusher.html', context)