"""Flask app configuration file."""
from os import environ, path

from dotenv import load_dotenv

# Specify an .env file containing config values.
cwd = path.abspath(path.dirname(__file__))
load_dotenv(path.join(cwd, ".env"))

# General config.
SECRET_KEY = environ.get("SECRET_KEY")
