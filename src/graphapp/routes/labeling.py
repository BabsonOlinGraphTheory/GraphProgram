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
def label():
    label = request.form["label"]
    if label == "":
        label = None
    else:
        label = int(label)
    labeling.set_label(int(request.form["v"]), label)
    return "label set"

@labeling_blueprint.route("/set", methods=['POST'])
def set_labeling():
    print("DOING THE THING")
    data = request.get_json()
    print(data)
    labeling.labels = data["labeling"]
    return "labels set"
