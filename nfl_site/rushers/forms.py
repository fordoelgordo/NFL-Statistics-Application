from django import forms

TEAM_CHOICES= [('all time','All Time'),]

class RushersForm(forms.Form):
    first_name = forms.CharField(label = 'First Name', max_length=100,required=True)
    last_name = forms.CharField(label = 'Last Name', max_length=100,required=True)

class TeamPickForm(forms.Form):
    team_name = forms.CharField(label = 'Top Rushers',required = False, widget=forms.Select(choices=TEAM_CHOICES) )