"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent labeler object and the Flask labeler Blueprint.
"""
#Flask imports
from flask import Blueprint, request

# Graphlib imports
from graphlib.labeler import LPolynomialLabeler

# Graphapp imports
from graphapp.routes.graph import graph
from graphapp.routes.labeling import labeling

# EXPORTS:
labeler = LPolynomialLabeler()
labeler_blueprint = Blueprint("labeler", __name__)

###############################################################################

# ROUTES:
@labeler_blueprint.route("/new/LPoly")
def new_poly():
    labeler = LPolynomialLabeler(request.form["constraints"])
    return "new labeler created"

@labeler_blueprint.route("/complete")
def complete_labeling():
    resp = {}
    first_check = labeler.confirm_labeling(graph, labeling)
    if not first_check[0]:
        resp["err"] = "Current labeling already invalid"
        resp["problems"] = first_check[1]
    else:
        new_labeling = labeler.complete_labeling(graph, labeling, request.form["min"], request.form["max"])
        if new_labeling:
            labeling = new_labeling
        else:
            resp["err"] = "No valid labeling found"
    resp["labels"] = labeling.labels
    return resp

@labeler_blueprint.route("/confirm")
def confirm_labeling():
    resp = {}
    first_check = labeler.confirm_labeling(graph, labeling)
    if not first_check[0]:
        resp["err"] = "Current labeling already invalid"
        resp["problems"] = first_check[1]
    else:
        resp = "Labeling is valid"
    return resp
