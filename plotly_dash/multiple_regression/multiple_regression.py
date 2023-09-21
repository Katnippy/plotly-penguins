from __future__ import annotations
import sys

from dash import Dash, dcc, html, Output, Input

sys.path.append("plotly_dash/")
from data_viz import MultipleRegression


# Run the Dash app inside of the Flask app. 
def init_dash_app(flask_app):
    dash_app = Dash(server=flask_app, name='Multiple regression',
                    url_base_pathname='/multiple_regression/')

    # Build components.
    title = dcc.Markdown(children='# Multiple regression.')
    graph = dcc.Graph(figure={})
    species_radio = dcc.RadioItems([
        {"label": "Adelie", "value": "'Adelie%'"},
        {"label": "Chinstrap", "value": "'Chinstrap%'"},
        {"label": "Gentoo", "value": "'Gentoo%'"}
        ],
        value="'Adelie%'",
        inline=True
        )
    first_explanatory_radio = dcc.RadioItems([
        {"label": "Culmen Length (mm)", "value": "culmen_length_mm"},
        {"label": "Culmen Depth (mm)", "value": "culmen_depth_mm"},
        {"label": "Flipper Length (mm)", "value": "flipper_length_mm"},
        {"label": "Body Mass (g)", "value": "body_mass_g"},
        {"label": "δ15N (‰)", "value": "delta_15_N_ppt"},
        {"label": "δ13C (‰)", "value": "delta_13_C_ppt"}
        ],
        value="body_mass_g",
        inline=True
        )
    second_explanatory_radio = dcc.RadioItems([
        {"label": "Culmen Length (mm)", "value": "culmen_length_mm"},
        {"label": "Culmen Depth (mm)", "value": "culmen_depth_mm"},
        {"label": "Flipper Length (mm)", "value": "flipper_length_mm"},
        {"label": "Body Mass (g)", "value": "body_mass_g"},
        {"label": "δ15N (‰)", "value": "delta_15_N_ppt"},
        {"label": "δ13C (‰)", "value": "delta_13_C_ppt"}
        ],
        value="culmen_length_mm",
        inline=True
        )
    response_radio = dcc.RadioItems([
        {"label": "Culmen Length (mm)", "value": "culmen_length_mm"},
        {"label": "Culmen Depth (mm)", "value": "culmen_depth_mm"},
        {"label": "Flipper Length (mm)", "value": "flipper_length_mm"},
        {"label": "Body Mass (g)", "value": "body_mass_g"},
        {"label": "δ15N (‰)", "value": "delta_15_N_ppt"},
        {"label": "δ13C (‰)", "value": "delta_13_C_ppt"}
        ],
        value="culmen_depth_mm",
        inline=True
        )

    # Customise page layout.
    dash_app.layout = html.Div([
        html.Div(title),
        html.Div(graph),
        html.Div(children=[
            html.H4("Filter by species", style={"display": "inline"}),
            species_radio
            ]),
        html.Div(children=[
            html.H4("First explanatory variable (x-axis)", 
                    style={"display": "inline"}),
            first_explanatory_radio
            ], className='first-explanatory-radio'),
        html.Div(children=[
            html.H4("Second explanatory variable (y-axis)", 
                    style={"display": "inline"}),
            second_explanatory_radio
            ], className='second-explanatory-radio'),    
        html.Div(children=[
            html.H4("Response variable (z-axis)", style={"display": "inline"}),
            response_radio
            ], className='response-radio')
        ])


    @dash_app.callback(
        Output(graph, component_property='figure'),
        Input(species_radio, component_property='value'),
        Input(first_explanatory_radio, component_property='value'),
        Input(second_explanatory_radio, component_property='value'),
        Input(response_radio, component_property='value')
        )
    def update_graphs(species: str, first_explanatory: str, 
                    second_explanatory: str, response: str) -> go.Figure():
        """Update the graph from user inputs.

        Take in the user's choice of penguin species and explanatory and 
        response variables and return a multiple regression 3D scattergraph.

        Params:
            species (str): The user's choice of penguin species.       
            first_explanatory (str): The user's choice for the first explanatory 
                variable.
            second_explanatory (str): The user's choice for the second
                explanatory variable.
            response (str): The user's choice for the response variable.

        Returns:
            `figure`, a Plotly Express 3D scattergraph (`go.Figure()`).
        """
        figure = MultipleRegression(species, first_explanatory, second_explanatory,
                                    response).build_query()

        return figure
    

    return dash_app