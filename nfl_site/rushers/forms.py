from django import forms

class RushersForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

class TeamPickForm(forms.Form):
    team_name = forms.CharField(
    label = 'Enter Team Name', 
    required = True )