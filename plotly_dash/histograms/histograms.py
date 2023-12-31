from __future__ import annotations
import sys

from dash import Dash, dcc, html, Output, Input

sys.path.append("plotly_dash/")
from data_viz import Histogram


# Run the Dash app inside of the Flask app.
def init_dash_app(flask_app):
    dash_app = Dash(server=flask_app, name='Histograms',
                    url_base_pathname='/histograms/',
                    assets_folder='plotly_dash/histograms/assets')

    # Build components.
    title = dcc.Markdown(children='# Histograms')
    graph = dcc.Graph(figure={})
    species_radio = dcc.RadioItems([
        {"label": "All species together", "value": ""},
        {"label": "Only Adelies", "value": " AND species LIKE 'Adelie%'"},
        {"label": "Only Chinstraps", "value": " AND species LIKE 'Chinstrap%'"},
        {"label": "Only Gentoos", "value": " AND species LIKE 'Gentoo%'"}
        ],
        value="",
        inline=True
        )
    sex_radio = dcc.RadioItems([
        {"label": "Both sexes together", "value": ""},
        {"label": "Only male", "value": " AND sex LIKE 'MALE'"},
        {"label": "Only female", "value": " AND sex LIKE 'FEMALE'"}
        ],
        value="",
        inline=True
        )
    variable_radio = dcc.RadioItems([
        {"label": "Culmen Length (mm)", "value": "culmen_length_mm"},
        {"label": "Culmen Depth (mm)", "value": "culmen_depth_mm"},
        {"label": "Flipper Length (mm)", "value": "flipper_length_mm"},
        {"label": "Body Mass (g)", "value": "body_mass_g"},
        {"label": "δ15N (‰)", "value": "delta_15_N_ppt"},
        {"label": "δ13C (‰)", "value": "delta_13_C_ppt"}
        ],
        value="flipper_length_mm",
        inline=True
        )

    # Customise page layout.
    dash_app.layout = html.Div([
        html.Div(title),
        html.Div(graph),
        html.Div(children=[
            html.H4("Filter by species", style={"display": "inline"}),
            species_radio
            ], className='species-radio'),
        html.Div(children=[
            html.H4("Filter by sex", style={"display": "inline"}),
            sex_radio
            ], className='sex-radio'),
        html.Div(children=[
            html.H4("Variable", style={"display": "inline"}),
            variable_radio
            ], className='variable-radio')
        ])


    @dash_app.callback(
        Output(graph, component_property='figure'),
        Input(species_radio, component_property='value'),
        Input(sex_radio, component_property='value'),
        Input(variable_radio, component_property='value')
        )
    def update_graph(species: str, sex: str, variable: str) -> go.Figure():
        """Update the graph from user inputs.

        Take in the user's choice of data visualisation filters and variable 
        and return a corresponding histogram.

        Params:
            species (str): The user's choice of species to filter by (or 
                not).
            sex (str): The user's choice of sex to filter by (or not).
            variable (str): The user's choice of variable.
        
        Returns:
            `figure`, a Plotly Express histogram (`go.Figure()`).
        """
        figure = Histogram(species, sex, variable).build_query()
        figure.update_layout(plot_bgcolor='rgba(255, 255, 255, 0.2)', 
                             paper_bgcolor='rgba(0, 0, 0, 0)')

        return figure


    return dash_app
