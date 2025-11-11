from flask import Flask

# This line creates the Flask web application
app = Flask(__name__)

# This line imports the routes to make them available to the app
from app import routes