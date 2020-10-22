from django.shortcuts import render
import pandas as pd
from combine import forms # Import forms module from response app

# Create your views here.
'''
Author: FSt.J
Code Comments: adding relative path variable to point to the directory location of my NFL datasets.
               For me, they're one directory above our project directory in a folder called nfl_data
'''
# NFL Data relative path
data_path = '../../nfl_data/'

# Function to convert decimal height to cleaner form
def conv_height(h):
    ft = int(divmod(h,12)[0])
    inch = round(int(divmod(h,12)[1]),0)
    if h == 0 or h == "" or h == " ":
        return ""
    else:
        return str(ft)+"'"+str(inch)+"\""

# Define a dict to map combine event header to clean name
COMBINE_DICT = {
    '': '', # Provide the option to not select a combine measurement
    'combineArm': 'Arm Length',
    'combine40yd': '40-yard dash',
    'combineVert': 'Vertical jump',
    'combineBench': 'Bench Press',
    'combineShuttle': 'Shuttle drill',
    'combineBroad': 'Broad Jump',
    'combine3cone': '3-Cone Drill',
    'combine60ydShuttle': '60-yard shuttle',
    'combineWonderlic':'Wonderlic',
}

# response/combine page rendering
def combine_page(request):
    form = forms.CombineForm()
    df_dict = []
    df_rec = []


    # Read in combine.csv dataset
    combine = pd.read_csv(data_path + 'combine.csv')
    combine['combineHeightConv'] = combine['combineHeight'].apply(lambda x: conv_height(x))

    # Set holding variables
    player_dict = {} # Store the player's ID and associated combine statistic
    player_first_name = ''
    player_last_name = ''
    combine_year = 0
    combine_event = ''
    combine_pos = ''

    if request.method == "POST": # Means someone filled out our form
        form = forms.CombineForm(request.POST)
        if form.is_valid(): 
            player_dict.clear()
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            combine_year = form.cleaned_data.get('combine_year')
            combine_event = form.cleaned_data.get('combine_event')
            combine_pos = form.cleaned_data.get('combine_pos')
            
            # Now we need to filter the combine data based on the values entered
            # FILTER 1: first name, last name, event are populated
            if player_first_name != "" and player_last_name != "" and str(combine_year) == "None" and combine_event != "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['nameLast'] == player_last_name) 
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college',combine_event]]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    COMBINE_DICT[combine_event]
                ]
            # FILTER 2: first name, last name populated only    
            elif player_first_name != "" and player_last_name != "" and str(combine_year) == "None" and combine_event == "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['nameLast'] == player_last_name)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 3: combine year populated ONLY
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event == "":
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year) 
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 4: combine year and combine position populated    
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event == "" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year) &
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 5: combine year, combine event populated
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event != "" and combine_pos == "":
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year)
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight', combine_event]]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                    COMBINE_DICT[combine_event]
                ]
            # FILTER 6: combine year, combine event, combine position populated
            elif player_first_name == "" and player_last_name == "" and str(combine_year) != "None" and combine_event != "" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['combineYear'] == combine_year) &
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combinePosition','position','college','combineHeightConv','combineWeight', combine_event]]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                    COMBINE_DICT[combine_event]
                ]
            # FILTER 7: combine position populated ONLY
            elif player_first_name == "" and player_last_name == "" and str(combine_year) == "None" and combine_event == "" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 8: first name ONLY, combine year, position
            elif player_first_name != "" and player_last_name == "" and str(combine_year) != "None" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['combineYear'] == combine_year) &
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 9: last name ONLY, combine year, position
            elif player_first_name != "" and player_last_name == "" and str(combine_year) != "None" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['nameLast'] == player_last_name) &
                        (combine['combineYear'] == combine_year) &
                        (combine['combinePosition'] == combine_pos)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 10: first name ONLY, combine year
            elif player_first_name != "" and player_last_name == "" and str(combine_year) != "None" and combine_pos == "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['combineYear'] == combine_year) 
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 11: last name ONLY, combine year
            elif player_first_name == "" and player_last_name != "" and str(combine_year) != "None" and combine_pos == "":
                combine_filtered = \
                    combine[
                        (combine['nameLast'] == player_last_name) &
                        (combine['combineYear'] == combine_year) 
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 12: first name ONLY, position group
            elif player_first_name != "" and player_last_name == "" and str(combine_year) == "None" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name) &
                        (combine['combinePosition'] == combine_pos) 
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 13: last name ONLY, position group
            elif player_first_name == "" and player_last_name != "" and str(combine_year) == "None" and combine_pos != "":
                combine_filtered = \
                    combine[
                        (combine['nameLast'] == player_first_name) &
                        (combine['combinePosition'] == combine_pos) 
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 14: first name ONLY
            elif player_first_name != "" and player_last_name == "":
                combine_filtered = \
                    combine[
                        (combine['nameFirst'] == player_first_name)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            # FILTER 15: last name ONLY
            elif player_first_name == "" and player_last_name != "":
                combine_filtered = \
                    combine[
                        (combine['nameLast'] == player_first_name)
                    ][['nameFirst','nameLast','combineYear','combinePosition','position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = [
                    'First Name',
                    'Last Name',
                    'Year',
                    'Combine Position',
                    'College Position',
                    'College',
                    'Height',
                    'Weight',
                ]
            df_dict = combine_filtered.to_dict()
            df_rec = combine_filtered.to_dict(orient='records')
        
    context = {'form': form, 'df_dict':df_dict, 'df_rec':df_rec}

    return render(request, 'combine/combine.html', context)
