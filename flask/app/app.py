import sys

from flask import Flask, render_template

sys.path.append("././")
# ? Can we make this a little bit prettier?
from plotly_dash.histograms import histograms
from plotly_dash.linear_regression import linear_regression
from plotly_dash.multiple_regression import multiple_regression

flask_app = Flask(__name__, instance_relative_config=False)
flask_app.config.from_pyfile("../config.py")

histograms.init_dash_app(flask_app)
linear_regression.init_dash_app(flask_app)
multiple_regression.init_dash_app(flask_app)


@flask_app.route("/")
def index():
    return render_template("index.html.j2")


@flask_app.route("/glossary/")
def glossary():
    return render_template("glossary.html.j2")


if __name__ == "__main__":
    flask_app.run(debug=True)
