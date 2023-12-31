"""A collection of graphs for visualising the palmerpenguins dataset.

Alongside a utils class and a shared function, this module contains three
classes each representing a type of graph for interactive data visualisation
based on the palmerpenguins dataset: a histogram (for normal and other
distributions), a scattergraph (for linear regression), and a 3D scattergraph
(for multiple regression).

Typical usage example:

    figure = Class(args).build_query()
"""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import logging
import pandas as pd
import numpy as np
import plotly.express as px
from math import sqrt
import statsmodels.api as sm
import plotly.graph_objects as go


class GraphUtils:
    """Labels and colours for graphs."""
    labels = {
        "culmen_length_mm": "Culmen Length (mm)",
        "culmen_depth_mm": "Culmen Depth (mm)",
        "flipper_length_mm": "Flipper Length (mm)",
        "body_mass_g": "Body Mass (g)",
        "delta_15_N_ppt": "δ15N (‰)",
        "delta_13_C_ppt": "δ13C (‰)",
        }
    colours = {
        "'Adelie%'": "deeppink",
        "'Chinstrap%'": "black",
        "'Gentoo%'": "darkorange",
        " AND sex LIKE 'MALE'": "green",
        " AND sex LIKE 'FEMALE'": "yellow"
        }
    

# ? Does this need to be split up into 2 separate functions?
def _create_dataframe(query: sqlalchemy.TextClause()) -> pd.DataFrame():
    """Create a dataframe by querying the database.

       With the query provided by build_query(), connect to the database
       and place the results in a dataframe. Finally, return the (cleaned) 
       dataframe.

       Params:
           query (`sqlalchemy.TextClause()`): A class representing an SQL
               query.

       Returns:
           df, a Pandas dataframe (`pd.Dataframe()`) with a column or columns
           for the user's chosen variable(s), species, etc.
    """
    try:
        engine = create_engine("sqlite:///plotly_dash/palmerpenguins.sq3")
        df = pd.read_sql_query(query, engine)
        df = df.replace(r"^\s*$", np.nan, regex=True)
        df = df.dropna()

        return df
    except OperationalError as e:
        logging.error(f"Can't connect to database: {e}")
    except SQLAlchemyError as e:
        logging.error(f"Unexpected SQLAlchemy error: {e}")


class Histogram:
    """A histogram."""
    def __init__(self, species: str, sex: str, variable: str):
        """Params:
               species (str): The user's choice of species to filter by (or 
                   not).
               sex (str): The user's choice of sex to filter by (or not).
               variable (str): The user's choice of variable.
        """
        self.species = species
        self.sex = sex
        self.variable = variable

        self.variable_label = GraphUtils.labels[variable]
        self.colours = GraphUtils.colours

    def build_query(self):
        """Build an SQL query from the user's chosen variable and filters.
        
           Build an SQL query from the user's chosen variable and filters (if 
           applicable) which is then passed to _create_graph().
           
           Returns:
               `fig` from create_graph().
        """
        # ! Be wary of f-strings and SQL injection.
        query = f"""SELECT {self.variable}
                    FROM palmerpenguins
                    WHERE 1=1"""
        if self.species and self.sex:
            query += self.species + self.sex
        elif self.species:
            query += self.species
        elif self.sex:
            query += self.sex
        else:
            pass
        query = text(query)

        return self._create_graph(query)

    def _create_graph(self, query: sqlalchemy.TextClause()) -> go.Figure():
        """Create a histogram.
           
           Create a histogram with the user's chosen variable on the x-axis and 
           probability on the y-axis and return it.
           
           Params:
               query (`sqlalchemy.TextClause()`): A class representing an SQL
                   query.

           Returns:
               `fig`, a Plotly Express histogram (`go.Figure()`).
        """
        df = _create_dataframe(query)
        sex_labels = {
            "": "",
            " AND sex LIKE 'MALE'": " Male",
            " AND sex LIKE 'FEMALE'": " Female"
        }
        species_labels = {
            "": "Adelie, Chinstrap, and Gentoo",
            " AND species LIKE 'Adelie%'": "Adelie",
            " AND species LIKE 'Chinstrap%'": "Chinstrap",
            " AND species LIKE 'Gentoo%'": "Gentoo"
        }

        # ! Plotly Express handles number of bins strangely...
        sqrt_of_data_points = int(sqrt(df.shape[0]))
        fig = px.histogram(df, x=self.variable, histnorm='probability',
                           nbins=sqrt_of_data_points)
        fig.update_layout(
            title=f'What is the Distribution of {self.variable_label} amongst'
                  f'{sex_labels[self.sex]} {species_labels[self.species]} '
                  'Penguins?',
            xaxis_title=self.variable_label,
            yaxis_title='Probability'
            )
        # ? Add colours for when a specific species and sex are both selected?
        fig.update_traces(
            marker_color=self.colours[self.species[18:]] if self.species else
            (self.colours[self.sex] if self.sex else "cornflowerblue")
            )

        return fig
    

class LinearRegression:
    """A linear regression."""
    def __init__(self, species: str, explanatory: str, response: str):
        """Params:
               species (str): The user's choice of penguin species.       
               explanatory (str): The user's choice for the explanatory 
                   variable.
               response (str): The user's choice for the response variable.
        """
        self.species = species
        self.explanatory = explanatory
        self.response = response

        self.explanatory_label = GraphUtils.labels[explanatory]
        self.response_label = GraphUtils.labels[response]
        self.species_colour = GraphUtils.colours[species]

    def build_query(self):
        """Build an SQL query from the user's chosen variables and species.
        
           Build an SQL query from the user's chosen variables and species
           which is then passed to _create_graph().
           
           Returns:
               `fig` from create_graph().
        """
        query = text(f"""SELECT {self.explanatory}, {self.response}
                         FROM palmerpenguins 
                         WHERE species 
                         LIKE {self.species}""")

        return self._create_graph(query)
    
    def _create_graph(self, query: sqlalchemy.TextClause()) -> go.Figure():
        """Create a linear regression scattergraph.
           
           Create a scattergraph with a least squares line of best fit from the
           x and y-axis values and return it.
           
           Params:
               query (`sqlalchemy.TextClause()`): A class representing an SQL
                   query.

           Returns:
               `fig`, a Plotly Express scattergraph (`go.Figure()`).
        """
        df = _create_dataframe(query)
        fig = px.scatter(df, x=self.explanatory, y=self.response,
                         trendline='ols')
        fig.update_layout(
            title=f'What is the Correlation between {self.species[1:-2]} '
                  f'{self.explanatory_label} and {self.response_label}?',
            xaxis_title=self.explanatory_label,
            yaxis_title=self.response_label)
        fig.update_traces(marker_color=self.species_colour)
        fig.data[0]["hovertemplate"] = (f"{self.explanatory_label}=""%{x}<br>"
                                        f"{self.response_label}=""%{y}"
                                        "<extra></extra>")
        
        x_slope = (
            px.get_trendline_results(fig).px_fit_results.iloc[0].params[1])
        y_intercept = (
            px.get_trendline_results(fig).px_fit_results.iloc[0].params[0])
        r_squared = (
            px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)
        fig.data[1]["hovertemplate"] = ("<b>OLS trendline</b><br>"
                                        f"{self.response_label} = "
                                        f"{x_slope:.8f} * "
                                        f"{self.explanatory_label} + "
                                        f"{y_intercept:.3f}<br>"
                                        f"R²={r_squared:.6f}<br><br>"
                                        f"{self.explanatory_label}=""%{x}<br>"
                                        f"{self.response_label}=""%{y:.4f}"
                                        "<b>(trend)</b>"
                                        "<extra></extra>")
        
        return fig
    

class MultipleRegression:
    """A multiple regression."""
    def __init__(self, species: str, first_explanatory: str, 
                 second_explanatory: str, response: str):
        """Params:
               species (str): The user's choice of penguin species.       
               first_explanatory (str): The user's choice for the first 
                   explanatory variable.
               second_explanatory (str): The user's choice for the second 
                   explanatory variable.
               response (str): The user's choice for the response variable.
        """
        self.species = species
        self.first_explanatory = first_explanatory
        self.second_explanatory = second_explanatory
        self.response = response

        self.first_explanatory_label = GraphUtils.labels[first_explanatory]
        self.second_explanatory_label = GraphUtils.labels[second_explanatory]
        self.response_label = GraphUtils.labels[response]
        self.species_colour = GraphUtils.colours[species]


    def build_query(self):
        """Build an SQL query from the user's chosen variables and species.
        
           Build an SQL query from the user's chosen variables and species
           which is then passed to _create_graph().
           
           Returns:
               `fig` from create_graph().
        """
        query = text(f"""SELECT {self.first_explanatory}, 
                                {self.second_explanatory},
                                {self.response}
                         FROM palmerpenguins 
                         WHERE species 
                         LIKE {self.species}""")

        return self._create_graph(query)

    def _create_graph(self, query: sqlalchemy.TextClause()) -> go.Figure():
        """Create a 3D scattergraph.
           
           Create a 3D scattergraph from the three variables and pass it and 
           the dataframe to _draw_plane().
           
           Params:
               query (`sqlalchemy.TextClause()`): A class representing an SQL
                   query.

           Returns:
               `fig` from draw_plane().
        """
        df = _create_dataframe(query)
        fig = px.scatter_3d(
            df,
            x=self.first_explanatory,
            y=self.second_explanatory,
            z=self.response,
            title=f'Can {self.species[1:-2]} '
                  f'{self.first_explanatory_label} and '
                  f'{self.second_explanatory_label} Help Predict '
                  f'{self.response_label}?',
            labels={
                self.first_explanatory: self.first_explanatory_label,
                self.second_explanatory: self.second_explanatory_label,
                self.response: self.response_label
                }
            )
        fig.update_traces(
            marker_size=4,
            marker_color=self.species_colour,
            marker_line_width=2,
            marker_line_color=
                'white' if self.species == "'Chinstrap%'" else 'black'
            )

        return self._fit_model(df, fig)
    
    def _fit_model(self, df: pd.DataFrame(), fig: go.Figure()) -> go.Figure():
        """Fit a multiple regression model.

           Fit a multiple regression model to the data using least squares.

           Params:
               df (`pd.DataFrame()`): A dataframe with 3 columns for the 
                   explanatory and response variables.
               fig (`go.Figure()`): A Plotly Express 3D scattergraph.
        
           Returns:
               `fig` from draw_plane().

        """
        first_explanatory = df[self.first_explanatory] # ! df[...] deprecated?
        second_explanatory = df[self.second_explanatory]
        response = df[self.response]
        X = pd.concat([first_explanatory, second_explanatory], axis=1)
        y = response
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()

        return self._draw_plane(first_explanatory, second_explanatory, model,
                               fig)
    
    def _draw_plane(
            self, 
            first_explanatory: pd.Series(),
            second_explanatory: pd.Series(),
            model: sm.regression.linear_model.RegressionResultsWrapper(),
            fig: go.Figure()
            ) -> go.Figure():
        """Draw a plane of best fit.

           From the multiple regression model, draw a plane of best fit to the
           graph and return it. 

           Params:
               first_explanatory (`pd.Series()`): A series for data 
                   corresponding to the first explanatory variable.
               second_explanatory (`pd.Series()`): A series for data 
                   corresponding to the second explanatory variable.
               model (`sm.regression.linear_model.RegressionResultsWrapper()`):
                   A summary of the statsmodels multiple regression from 
                   _fit_model().
               fig (`go.Figure()`): A Plotly Express 3D scattergraph.

           Returns:
               `fig`, a Plotly Express 3D scattergraph (`go.Figure()`).
        """
        z_intercept = model.params[0]
        x_slope = model.params[1]
        y_slope = model.params[2]
        xx1, xx2 = np.meshgrid(
            np.linspace(first_explanatory.min(), first_explanatory.max()),
            np.linspace(second_explanatory.min(), second_explanatory.max())
            )
        z = z_intercept + (x_slope * xx1) + (y_slope * xx2)

        # ! Equation text makes the hover box quite lengthy.
        fig.add_trace(go.Surface(
            x=xx1,
            y=xx2,
            z=z,
            hovertemplate='<b>OLS plane</b><br>'
                          f'{self.response_label} = {x_slope:.8f} * '
                          f'{self.first_explanatory_label} + {y_slope:.8f} * '
                          f'{self.second_explanatory_label} + '
                          f'{z_intercept:.3f}'
                          f'<br>Adjusted R²={model.rsquared_adj:.6f}<br><br>'
                          f'{self.first_explanatory_label}=''%{x:.4f}<br>'
                          f'{self.second_explanatory_label}=''%{y:.4f}<br>'
                          f'{self.response_label}=''%{z:.4f} '
                          '<b>(trend)</b><extra></extra>',
            colorscale='spectral',
            colorbar=dict(title=f'Predicted {self.response_label}')
            ))

        return fig
