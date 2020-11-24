from django import forms
from django.core import validators

# Define years that the combine was held to select from
COMBINE_YEARS = [tuple([x,x]) for x in range(2004, 2020)]
COMBINE_YEARS.insert(0, ('', ''))

# Form to enter NFL year in which to review standings
class YearForm(forms.Form):
    year_val = forms.IntegerField(label = 'Select combine year', required = False, widget = forms.Select(choices=COMBINE_YEARS))
    
    # This is extra protection code to prevent a bot from entering bogus info on your site
    bot_catcher = forms.CharField(required=False, 
                                  widget=forms.HiddenInput, # Field won't show up on page for user, will be in background HTML
                                  validators=[validators.MaxLengthValidator(0)]) # Ensure a bot didn't fill in something