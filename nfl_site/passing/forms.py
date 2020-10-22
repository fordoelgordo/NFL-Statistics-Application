from django import forms
from django.core import validators


PASSING_YEARS = [tuple([x,x]) for x in range(1987, 2020)]
PASSING_YEARS.insert(0, ('', ''))

PASSING_OUTCOME = [
    ('',''),
    ('complete', 'Complete'), 
    ('incomplete', 'Incomplete'), 
    ('interception', 'Interception'),
    ('sack', 'Sack')
    ]

class PassingForm(forms.Form):
    player_name = forms.CharField(label = 'Enter Player\'s Name', required = False)
    passing_year = forms.IntegerField(label = 'Select Year', required = False, widget = forms.Select(choices=PASSING_YEARS))
    passing_outcome = forms.CharField(label = 'Select Passing Outcome', required = False, widget = forms.Select(choices=PASSING_OUTCOME))
    passing_length = forms.IntegerField(label = 'Enter Passing Length (Yards)', required = False)
