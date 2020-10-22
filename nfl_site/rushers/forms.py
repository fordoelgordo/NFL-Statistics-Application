from django import forms

class RushersForm(forms.Form):
    player_name = forms.CharField(max_length=100)