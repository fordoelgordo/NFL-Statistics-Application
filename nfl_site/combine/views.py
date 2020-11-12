from django.shortcuts import render
from combine import forms # Import forms module from combine app
from nfl_site.libraries import csv_to_dict, conv_height, mean, stddev # Get user functions
from pathlib import Path
import pandas as pd
# Dava viz packages
import plotly.offline as plot
import plotly.express as px
import plotly.graph_objects as go

# Create your views here.

# NFL Data relative path
data_path = 'static/archive/'

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

# Read in the combine.csv data using Rob's CSV reader function
combine = ""
if Path(data_path).exists():
    combine = csv_to_dict(data_path + 'combine.csv', to_df = 1)
    combine['combineHeightConv'] = combine['combineHeight'].apply(lambda x: conv_height(float(x)))
    combine['combineYear'] = combine['combineYear'].apply(lambda x: int(x))
    for measure in COMBINE_DICT:
        if measure != '':
            combine[measure] = combine[measure].apply(lambda x: float(x) if x != None else x)
            
# response/combine page rendering
def combine_page(request):
    form = forms.CombineForm()
    statistics = forms.CombineStats()
    df_dict = []
    df_rec = []

    # Set holding variables
    player_first_name = ''
    player_last_name = ''
    combine_year = 0
    combine_event = ''
    combine_pos = ''
    num_players = 1
    user_stat = ""
    avg = 0
    sd = 0
    out_high = 0
    out_low = 0
    weight_fig = ""
    height_fig = ""
    hist_fig = ""

    # Holding variables for the data figures
    scat_fig = ""
    data_viz = combine

    if request.method == "POST": # Means someone filled out our form
        form = forms.CombineForm(request.POST)
        statistics = forms.CombineStats(request.POST)
        if form.is_valid(): 
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            combine_year = form.cleaned_data.get('combine_year')
            combine_event = form.cleaned_data.get('combine_event')
            combine_pos = form.cleaned_data.get('combine_pos')
            if statistics.is_valid():
                num_players = statistics.cleaned_data.get('num_players')
                user_stat = statistics.cleaned_data.get('statistic')
            combine_filtered = combine

            # Filter the data based on player entries
            if player_first_name:
                combine_filtered = combine_filtered[combine_filtered['nameFirst'] == player_first_name]
            if player_last_name:
                combine_filtered = combine_filtered[combine_filtered['nameLast'] == player_last_name]
            if combine_year:
                combine_filtered = combine_filtered[combine_filtered['combineYear'] == combine_year]
            if combine_pos:
                combine_filtered = combine_filtered[combine_filtered['combinePosition'] == combine_pos]
            if combine_event:
                combine_filtered = combine_filtered[['playerId','combineYear','nameFirst','nameLast','combinePosition', 'position','college','combineHeightConv','combineWeight', combine_event]]
                combine_filtered.columns = ['Player ID','Year','First Name','Last Name','Combine Position','Collge Position','College','Height','Weight', COMBINE_DICT[combine_event]]
                avg = mean(combine_filtered, COMBINE_DICT[combine_event])
                sd = stddev(combine_filtered, COMBINE_DICT[combine_event])
                if user_stat:
                    # Filter to players above the average ("above average" depends on the event, e.g. a 40-time < the average is considered above average)
                    if user_stat == 'aa':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] > avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                        else:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] < avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                    # Filter to players below the average
                    if user_stat == 'ba':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] < avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                        else:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] > avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                    # Filter to players who's performance was an outlier
                    if user_stat == 'o':
                        out_high = avg + (3 * sd)
                        out_low = avg - (3 * sd)
                        combine_filtered = combine_filtered[(combine_filtered[COMBINE_DICT[combine_event]] < out_low) | (combine_filtered[COMBINE_DICT[combine_event]] > out_high)]
                    # Filter top players - top and bottom differ depending on the event
                    if user_stat == 't':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                        else:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                        if num_players:
                            combine_filtered = combine_filtered.head(n=num_players)
                    # Filter bottom players
                    if user_stat == 'b':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                        else:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                        if num_players:
                            combine_filtered = combine_filtered.head(n=num_players)
                # Simply restrict the view to the number of players selected
                if num_players:
                    combine_filtered = combine_filtered.head(n=num_players)
            else:
                combine_filtered = combine_filtered[['playerId','combineYear','nameFirst','nameLast','combinePosition', 'position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = ['Player ID','Year','First Name','Last Name','Combine Position','Collge Position','College','Height','Weight']
            df_dict = combine_filtered.to_dict()
            df_rec = combine_filtered.to_dict(orient='records')
            avg = round(avg, 2)
            sd = round(sd, 2)
            out_high = avg + (3 * sd)
            out_low = avg - (3 * sd)

            # Code below is to create a scatterplot of wide receiver times vs their weight
            if combine_event:
                # Get rid of the NaNs
                data_viz = combine_filtered
                data_viz.dropna(subset=[COMBINE_DICT[combine_event]], inplace = True)
                # Some of the combine measures had no valid values for a particular combine year or position group
                if (len(data_viz) > 0):
                    data_viz['Name'] = data_viz['First Name'] + ' ' + data_viz['Last Name']
                    
                    # Histogram annotated with the average
                    fig = go.Figure()
                    fig.add_trace(go.Histogram(
                        x=data_viz[COMBINE_DICT[combine_event]],
                        name=COMBINE_DICT[combine_event],
                        marker_color='black',
                        opacity=0.75
                    ))
                    fig.update_layout(
                        title_text='Histogram of {}'.format(COMBINE_DICT[combine_event]),
                        xaxis_title_text='Value',
                        yaxis_title_text='Count',
                        bargap=0.1,
                        bargroupgap=0.1,
                        font={'family':'Arial','color':'blue'}
                    )
                    fig.add_shape(
                        go.layout.Shape(type='line',xref='x', x0=avg, y0=0, x1=avg, y1=12, line={'dash':'dash','color':'red'})
                    )
                    fig.add_annotation(
                        x=avg,
                        y=12,
                        text="Avg. {}: {}".format(COMBINE_DICT[combine_event], round(avg,2)),
                        font={'color':'red'},
                        arrowhead=2
                    )
                    hist_fig = plot.plot(fig, output_type='div')

                    # Plot the combine event score vs. weight
                    fig = px.scatter(data_viz, x='Weight',y=COMBINE_DICT[combine_event],color='Name',title="Weight vs. {}".format(COMBINE_DICT[combine_event]), 
                    labels={'Name':'Player Name',
                            'Weight':'Weight (lbs)'})
                    fig.update_xaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_yaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_traces(marker=dict(
                        size=13,
                        line=dict(width=1.5,color='DarkSlateGrey')),
                    )
                    fig.update_layout(showlegend=False, title_text="Weight vs. {}".format(COMBINE_DICT[combine_event]), title_font=dict(size=18, family='Arial', color='Blue'))
                    weight_fig = plot.plot(fig, output_type='div')
                    
                    # Plot the combine event score vs. height
                    data_viz.Height = pd.Categorical(data_viz.Height, categories=[
                        "5\'6\"","5\'7\"","5\'8\"","5\'9\"","5\'10\"","5\'11\"","6\'0\"","6\'1\"","6\'2\"","6\'3\"","6\'4\"","6\'5\"","6\'6\"","6\'7\"","6\'8\""
                    ],
                    ordered = True)
                    data_viz.sort_values('Height', inplace = True)
                    fig = px.scatter(data_viz, x='Height',y=COMBINE_DICT[combine_event],color='Name',title="Height vs. {}".format(COMBINE_DICT[combine_event]), 
                    labels={'Name':'Player Name',
                            'Height':'Height (U.S. standard)'})
                    fig.update_xaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_yaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_traces(marker=dict(
                        size=13,
                        line=dict(width=1.5,color='DarkSlateGrey')),
                    )
                    fig.update_layout(showlegend=False, title_text="Height vs. {}".format(COMBINE_DICT[combine_event]), title_font=dict(size=18, family='Arial', color='Blue'))
                    height_fig = plot.plot(fig, output_type='div')
                    

    context = {'form': form, 'statistics': statistics, 'df_dict':df_dict, 'df_rec':df_rec, 'avg':avg, 'std':sd, 'stat':user_stat, 'out_high':out_high, 'out_low':out_low, 'hist_fig':hist_fig, 'weight_fig':weight_fig,'height_fig':height_fig}

    return render(request, 'combine/combine.html', context)
