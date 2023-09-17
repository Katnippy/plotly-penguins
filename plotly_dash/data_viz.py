#
# TODO: Need docstring describing this module.
""""""

from __future__ import annotations

from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import plotly.express as px
from math import sqrt

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

        return self.create_dataframe(query)

    # ? Does this need to be split up into 2 separate functions?
    def create_dataframe(self, query: sqlalchemy.TextClause()) -> go.Figure():
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

        return self.create_graph(df)

    def create_graph(self, df: pd.DataFrame()) -> go.Figure():
        """Create a histogram.
           
           Create a histogram with the user's chosen variable on the x-axis and 
           probability on the y-axis and return it.
           
           Params:
               df (`pd.Dataframe()`): A dataframe with a single column for the 
                   user's chosen variable.

           Returns:
               `fig`, a Plotly Express histogram (`go.Figure()`).
        """
        fig = px.histogram(df, x=self.variable, histnorm='probability',
                           nbins=int(sqrt(df.shape[0])))

        return fig
