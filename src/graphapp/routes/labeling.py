"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent labeling object and the Flask labeling Blueprint.
"""
#Flask imports
from flask import Blueprint, request

# Graphlib imports
from graphlib.labeling import Labeling

# EXPORTS:
labeling = Labeling()
labeling_blueprint = Blueprint("labeling", __name__)

###############################################################################

# ROUTES:
@labeling_blueprint.route("/label", methods=['POST'])
def new():
    labeling.set_label(int(request.form["v"]), int(request.form["label"]))
    return "label set"
