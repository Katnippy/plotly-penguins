#
# TODO: Need docstring describing this module.
""""""

from __future__ import annotations

from sqlalchemy import create_engine, text
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
        "'Gentoo%'": "darkorange"
        }


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

    def build_query(self):
        """Build a SQL query from the user's chosen variable and filters.
        
           Build a SQL query from the user's chosen variable and filters (if 
           applicable) which is then passed to create_dataframe().
           
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

        return self._create_dataframe(query)

    # TODO: Handle exception(s) if connection / query fails.
    # ? Does this need to be split up into 2 separate functions?
    # ? This method can be found in the 2 other functions. Can we do anything
    # ? about that?
    def _create_dataframe(self, query: sqlalchemy.TextClause()) -> go.Figure():
        """Create a dataframe by querying the database.

           With the query provided by build_query(), connect to the database
           and place the results in a dataframe. Finally, pass the (clean) 
           dataframe to create_graph().

           Params:
               query (`sqlalchemy.TextClause()`): A class representing a SQL
                   query.

           Returns:
               `fig` from create_graph().
        """
        engine = create_engine("sqlite:///plotly_dash/palmerpenguins.sq3")
        df = pd.read_sql_query(query, engine)
        df = df.replace(r"^\s*$", np.nan, regex=True)
        df = df.dropna()

        return self._create_graph(df)

    def _create_graph(self, df: pd.DataFrame()) -> go.Figure():
        """Create a histogram.
           
           Create a histogram with the user's chosen variable on the x-axis and 
           probability on the y-axis and return it.
           
           Params:
               df (`pd.Dataframe()`): A dataframe with a single column for the 
                   user's chosen variable.

           Returns:
               `fig`, a Plotly Express histogram (`go.Figure()`).
        """
        # ! Plotly Express handles number of bins strangely...
        sqrt_of_data_points = int(sqrt(df.shape[0]))
        fig = px.histogram(df, x=self.variable, histnorm='probability',
                           nbins=sqrt_of_data_points)

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

    def build_query(self):
        """Build a SQL query from the user's chosen variables and species.
        
           Build a SQL query from the user's chosen variables and species
           which is then passed to create_dataframe().
           
           Returns:
               `fig` from create_graph().
        """
        query = text(f"""SELECT {self.explanatory}, {self.response}
                         FROM palmerpenguins 
                         WHERE species 
                         LIKE {self.species}""")

        return self._create_dataframe(query)
    
    def _create_dataframe(self, query: sqlalchemy.TextClause()) -> go.Figure():
        """Create a dataframe by querying the database.

           With the query provided by build_query(), connect to the database
           and place the results in a dataframe. Finally, pass the (clean) 
           dataframe to create_graph().

           Params:
               query (`sqlalchemy.TextClause()`): A class representing a SQL
                   query.

           Returns:
               `fig` from create_graph().
        """
        engine = create_engine("sqlite:///plotly_dash/palmerpenguins.sq3")
        df = pd.read_sql_query(query, engine)
        df = df.replace(r"^\s*$", np.nan, regex=True)
        df = df.dropna()

        return self._create_graph(df)
    
    def _create_graph(self, df: pd.DataFrame()) -> go.Figure():
        """Create a linear regression scattergraph.
           
           Create a scattergraph with a least squares line of best fit from the
           x and y-axis values and return it.
           
           Params:
               df (`pd.Dataframe()`): A dataframe with 2 columns for the x and 
                   y-axis values.

           Returns:
               `fig`, a Plotly Express scattergraph (`go.Figure()`).
        """
        fig = px.scatter(df, x=self.explanatory, y=self.response,
                         trendline='ols')

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

        self.first_explanatory_label = (
            GraphUtils.labels[self.first_explanatory])
        self.second_explanatory_label = (
            GraphUtils.labels[self.second_explanatory])
        self.response_label = GraphUtils.labels[self.response]
        self.species_colour = GraphUtils.colours[self.species]


    def build_query(self):
        """Build a SQL query from the user's chosen variables and species.
        
           Build a SQL query from the user's chosen variables and species
           which is then passed to create_dataframe().
           
           Returns:
               `fig` from create_graph().
        """
        query = text(f"""SELECT {self.first_explanatory}, 
                                {self.second_explanatory},
                                {self.response}
                         FROM palmerpenguins 
                         WHERE species 
                         LIKE {self.species}""")

        return self._create_dataframe(query)
    
    def _create_dataframe(self, query: sqlalchemy.TextClause()) -> go.Figure():
        """Create a dataframe by querying the database.

           With the query provided by build_query(), connect to the database
           and place the results in a dataframe. Finally, pass the (clean) 
           dataframe to create_graph().

           Params:
               query (`sqlalchemy.TextClause()`): A class representing a SQL
                   query.

           Returns:
               `fig` from create_graph().
        """
        engine = create_engine("sqlite:///plotly_dash/palmerpenguins.sq3")
        df = pd.read_sql_query(query, engine)
        df = df.replace(r"^\s*$", np.nan, regex=True)
        df = df.dropna()

        return self._create_graph(df)

    def _create_graph(self, df: pd.DataFrame()) -> go.Figure():
        """Create a 3D scattergraph.
           
           Create a 3D scattergraph from the three variables and pass it and 
           the dataframe to draw_plane().
           
           Params:
               df (`pd.DataFrame()`): A dataframe with 3 columns for the 
                   explanatory and response variables.

           Returns:
               `fig` from draw_plane().
        """
        fig = px.scatter_3d(
            df,
            x=self.first_explanatory,
            y=self.second_explanatory,
            z=self.response,
            labels={
                self.first_explanatory: self.first_explanatory_label,
                self.second_explanatory: self.second_explanatory_label,
                self.response: self.response_label
                }
            )
        fig.update_traces(
            marker=dict(
                size=4,
                color=self.species_colour,
                line=dict(
                    width=2,
                    color='white' if self.species == "'Chinstrap%'"
                        else 'black')
                )
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
               first_explanatory (`pd.Series()`): ...
               second_explanatory (`pd.Series()`): ...
               model (`sm.regression.linear_model.RegressionResultsWrapper()`):
                   ...
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

        # ! Equation text is quite lengthy.
        # ? hovertemplate code isn't very human-readable.
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
            colorscale='haline',
            colorbar=dict(title=f'Predicted {self.response_label}')
            ))

        return fig