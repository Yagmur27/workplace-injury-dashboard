# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13SbC_Z9ae8P3y6XhGsJsU0RY24QHBUMX
"""

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import os

# Load dataset
file_path = "Cleaned_Workplace_Injury_Data2_With_LatLong.csv"  # Ensure this file is in the same folder
df = pd.read_csv(file_path)

# Initialize Dash app
app = dash.Dash(__name__)

# Dropdown options
state_options = [{'label': state, 'value': state} for state in df['state'].unique()]
industry_options = [{'label': industry, 'value': industry} for industry in df['industry_description'].dropna().unique()]
incident_options = [{'label': incident, 'value': incident} for incident in df['type_of_incident'].dropna().unique()]

# Define Dash app layout
app.layout = html.Div([
    html.H1("Workplace Injury Dashboard", style={'textAlign': 'center'}),

    # Filters
    html.Div([
        html.Label("Filter by State:"),
        dcc.Dropdown(id="state-dropdown", options=state_options, multi=True, placeholder="Select states..."),

        html.Label("Filter by Industry:"),
        dcc.Dropdown(id="industry-dropdown", options=industry_options, multi=True, placeholder="Select industries..."),

        html.Label("Filter by Incident Type:"),
        dcc.Dropdown(id="incident-dropdown", options=incident_options, multi=True, placeholder="Select injury types..."),
    ], style={'width': '80%', 'margin': '10px auto'}),

    # Scatter Map
    dcc.Graph(id="scatter-map"),
])

# Callback to update scatter map based on filters
@app.callback(
    Output("scatter-map", "figure"),
    [Input("state-dropdown", "value"),
     Input("industry-dropdown", "value"),
     Input("incident-dropdown", "value")]
)
def update_map(selected_states, selected_industries, selected_incidents):
    # Apply filters
    filtered_df = df.copy()
    if selected_states:
        filtered_df = filtered_df[filtered_df['state'].isin(selected_states)]
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industry_description'].isin(selected_industries)]
    if selected_incidents:
        filtered_df = filtered_df[filtered_df['type_of_incident'].isin(selected_incidents)]

    # Create updated scatter map
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        hover_data=["state", "type_of_incident", "industry_description"],
        color="type_of_incident",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        zoom=3,
        height=700
    )

    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0, "t":0, "l":0, "b":0})

    return fig_map

# Run Dash app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000, debug=False)