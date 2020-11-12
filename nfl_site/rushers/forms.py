from django import forms
from .nfldata import readTeams

team_names = sorted(readTeams()['draftTeam'].to_list())

TEAM_CHOICES= [('all time','All Time'),]
team_num = 1
for name in team_names:
    TEAM_CHOICES.append((str(team_num),name))
    team_num = team_num + 1

class RushersForm(forms.Form):
    first_name = forms.CharField(label = 'First Name', max_length=100,required=True)
    last_name = forms.CharField(label = 'Last Name', max_length=100,required=True)

class TeamPickForm(forms.Form):
    team_name = forms.CharField(label = 'Top Rushers',required = True, widget=forms.Select(choices=TEAM_CHOICES) )