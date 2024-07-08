# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

spacex_df.values
spacex_df.rename(columns = {'class':'class_'}, inplace = True)
#spacex_df.class_ = spacex_df.class_.astype(str)
#spacex_df['class_'].replace('0', 'failed', inplace=True)
#spacex_df['class_'].replace('1', 'success', inplace=True)

print (spacex_df)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                    dcc.Dropdown(id='site-dropdown',
                                        options=[{'label': 'All Sites', 'value': 'ALL'}, {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},],
                                        value='ALL',
                                        placeholder="place holder here",
                                        searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(0, 10000, 1000, value=[0, 10000], id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        print(filtered_df)
        if entered_site == 'ALL':
            fig = px.pie(spacex_df, values='class_', names='Launch Site', title='Total Success Launches By Site')
            return fig
        elif entered_site == 'CCAFS LC-40':
            fig = px.pie(filtered_df, values='class_', names='class_', title='Total Success Launches for ' + entered_site)
            return fig
        elif entered_site == 'CCAFS SLC-40':
            fig = px.pie(filtered_df, values='class_', names='class_', title='Total Success Launches for ' + entered_site)
            return fig
        elif entered_site == 'KSC LC-39A':
            fig = px.pie(filtered_df, values='class_', names='class_', title='Total Success Launches for ' + entered_site)
            return fig
        elif entered_site == 'VAFB SLC-4E':
            fig = px.pie(filtered_df, values='class_', names='class', title='Total Success Launches for ' + entered_site)
            return fig
        else:
            return fig
# return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
#@callback( Output('payload-slider', 'children'), Input('my-range-slider', 'value'))
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), Input(component_id='payload-slider', component_property='value'))
def get_range_slider(entered_payload_mass):
    low_entered_payload_mass, high_entered_payload_mass = entered_payload_mass
    print ('low_entered_payload_mass: '+ str(low_entered_payload_mass))
    print ('high_entered_payload_mass: '+ str(high_entered_payload_mass))
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] >= low_entered_payload_mass]
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] <= high_entered_payload_mass]
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="Launch Site", color="class_")
    return fig


# Run the app
 
if __name__ == '__main__':
    app.run_server()