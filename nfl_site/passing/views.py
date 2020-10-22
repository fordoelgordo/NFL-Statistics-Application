from django.shortcuts import render
from passing import forms

import pandas as pd

_DATA_PATH = '/Users/kdean/Documents/Dev/cs180/cs180project-021-team-42/archive/'

# Create your views here.
def pass_page(request):
    form = forms.PassingForm()
    pass_df = pd.read_csv(f'{_DATA_PATH}passer.csv')
    players_df = pd.read_csv(f'{_DATA_PATH}players.csv')

    # Set holding variables
    pass_dict = {}

    if request.method == "POST": # Means someone filled out our form
        form = forms.PassingForm(request.POST)

        if form.is_valid():
            player_name = form.cleaned_data.get('player_name').title()
            passing_year = form.cleaned_data.get('passing_year')
            passing_outcome = form.cleaned_data.get('passing_outcome')
            passing_length = form.cleaned_data.get('passing_length')

            if player_name:
                name_filter = players_df.loc[(players_df['nameFirst'] == player_name.split()[0]) & (players_df['nameLast'] == player_name.split()[1])]
                if len(name_filter) == 0:
                    return render(request,'passing/passing.html', {'form': form, 'empty': 'Player Does Not Exist!'})

              
            if player_name != "" and str(passing_year) == "None" and passing_outcome != "" and str(passing_length) != 'None':
                #print(1)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & (pass_df['passOutcomes'].values == passing_outcome) & (pass_df['passLength'].values == passing_length)]

            elif player_name != "" and str(passing_year) == "None" and passing_outcome == "" and str(passing_length) != 'None': 
                #print(2)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & (pass_df['passLength'].values == passing_length)]

            elif player_name != "" and str(passing_year) == "None" and passing_outcome != '': 
                #print(3)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values) & (pass_df['passOutcomes'].values == passing_outcome)]

            elif player_name != "" and str(passing_year) == "None":
                #print(4)
                pass_dict = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

          

    if len(pass_dict) != 0:
        return render(request,'passing/passing.html', {'form': form, 'pass': pass_dict, 'columns' : pass_df.columns})
    else:
        return render(request,'passing/passing.html', {'form': form})