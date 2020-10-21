from django import forms
from django.core import validators

# Custom validator - an example of how you can create your own function to validate form entries
''' Example code, commented out
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Needs to start with lowercase z")
'''
# Define combine events that are present in the combine.csv dataset
COMBINE_EVENTS = [
    ('', ''), # Provide the option to not select a combine measurement
    ('combineArm', 'Arm Length'),
    ('combine40yd', '40-yard dash'),
    ('combineVert', 'Vertical jump'),
    ('combineBench', 'Bench Press'),
    ('combineShuttle', 'Shuttle drill'),
    ('combineBroad', 'Broad Jump'),
    ('combine3cone', '3-Cone Drill'),
    ('combine60ydShuttle', '60-yard shuttle'),
    ('combineWonderlic', 'Wonderlic'),
]

# Define years that the combine was held to select from
COMBINE_YEARS = [tuple([x,x]) for x in range(1987, 2020)]
COMBINE_YEARS.insert(0, ('', ''))

# Form object that we will render to receive input
class CombineForm(forms.Form):
    player_first_name = forms.CharField(label = 'Enter player first name', required = False)
    player_last_name = forms.CharField(label = 'Enter player last name', required = False)
    combine_year = forms.IntegerField(label = 'Select combine year', required = False, widget = forms.Select(choices=COMBINE_YEARS))
    combine_event = forms.CharField(label = 'Select combine measurement', required = False, widget = forms.Select(choices=COMBINE_EVENTS))
    
    # This is extra protection code to prevent a bot from entering bogus info on your site
    bot_catcher = forms.CharField(required=False, 
                                  widget=forms.HiddenInput, # Field won't show up on page for user, will be in background HTML
                                  validators=[validators.MaxLengthValidator(0)]) # Ensure a bot didn't fill in something
   
    ''' Example code of how to ensure required fields match
    def clean(self):
        all_clean_data = super().clean() # return all clean data for the form
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError("Make sure emails match")   
    '''