"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This is the main Flask app backend for the graph labeling GUI
"""

# Flask imports
from flask import Flask, render_template

# Routing imports
from graphapp.routes.labeling import labeling_blueprint
from graphapp.routes.graph import graph_blueprint
from graphapp.routes.labeler import labeler_blueprint

# Create the flask app and register blueprints
app = Flask("graphapp")
app.register_blueprint(graph_blueprint, url_prefix="/graph")
app.register_blueprint(labeler_blueprint, url_prefix="/labeler")
app.register_blueprint(labeling_blueprint, url_prefix="/labeling")


# Render landing page
@app.route('/')
def home():
    return render_template("index.html")

# Serve js files
@app.route('/javascripts/<path:path>')
def serve_static(path):
    return app.send_static_file('javascripts/'+path)