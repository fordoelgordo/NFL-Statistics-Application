from django import forms

FRUIT_CHOICES= [('all time','All Time'),]

class RushersForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

class TeamPickForm(forms.Form):
    team_name = forms.CharField( label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES) )