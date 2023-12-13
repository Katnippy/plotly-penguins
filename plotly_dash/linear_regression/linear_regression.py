from __future__ import annotations

from dash import Dash, dcc, html, Output, Input

from data_viz import LinearRegression


# Run the Dash app inside of the Flask app. 
def init_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, 
                    url_base_pathname='/linear_regression/')

    # Build components.
    title = dcc.Markdown(children='# Linear regression')
    graph = dcc.Graph(figure={})
    species_radio = dcc.RadioItems([
        {"label": "Adelie", "value": "'Adelie%'"},
        {"label": "Chinstrap", "value": "'Chinstrap%'"},
        {"label": "Gentoo", "value": "'Gentoo%'"}
        ],
        value="'Adelie%'",
        inline=True
        )
    explanatory_radio = dcc.RadioItems([
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
    response_radio = dcc.RadioItems([
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
            html.H4("Explanatory variable (x-axis)", 
                    style={"display": "inline"}),
            explanatory_radio
            ], className='explanatory-radio'),
        html.Div(children=[
            html.H4("Response variable (y-axis)", style={"display": "inline"}),
            response_radio
            ], className='response-radio')
        ])


    @dash_app.callback(
        Output(graph, component_property='figure'),
        Input(species_radio, component_property='value'),
        Input(explanatory_radio, component_property='value'),
        Input(response_radio, component_property='value')
        )
    def update_graph(species: str, explanatory: str, 
                     response: str) -> go.Figure():
        """Update the graph from user inputs.

        Take in the user's choice of penguin species and x and y-axis variables 
        and return a corresponding linear regression scattergraph.

        Params:
            species (str): The user's choice of penguin species.       
            explanatory (str): The user's choice for the explanatory variable.
            response (str): The user's choice for the response variable.

        Returns:
            `figure`, a Plotly Express scattergraph (`go.Figure()`).
        """
        figure = LinearRegression(species, explanatory, response).build_query()
        figure.update_layout(plot_bgcolor='rgba(255, 255, 255, 0.2)', 
                             paper_bgcolor='rgba(0, 0, 0, 0)')

        return figure
    

    return dash_app
