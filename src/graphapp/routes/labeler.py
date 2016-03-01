"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent labeler object and the Flask labeler Blueprint.
"""
#Flask imports
from flask import Blueprint, request, jsonify

# Graphlib imports
from graphlib.labeler import LPolynomialLabeler

# Graphapp imports
import graphapp.routes.labeling as l
import graphapp.routes.graph as g

# EXPORTS:
labeler = LPolynomialLabeler()
labeler_blueprint = Blueprint("labeler", __name__)

###############################################################################

# ROUTES:
@labeler_blueprint.route("/new/LPoly", methods=['POST'])
def new_poly():
    global labeler;
    labeler = LPolynomialLabeler(request.form["constraints"])
    return "new labeler created"

@labeler_blueprint.route("/complete", methods=['POST'])
def complete_labeling():
    resp = {}
    first_check = labeler.confirm_labeling(g.graph, l.labeling)
    if not first_check[0]:
        resp["err"] = "Current labeling already invalid"
        resp["problems"] = first_check[1]
    else:
        new_labeling = labeler.complete_labeling(g.graph, l.labeling, int(request.form["min"]), int(request.form["max"]))
        print(new_labeling.labels)
        if new_labeling:
            l.labeling = new_labeling
        else:
            resp["err"] = "No valid labeling found"
    resp["labels"] = l.labeling.labels
    print(resp)
    return jsonify(resp)

@labeler_blueprint.route("/confirm", methods=['POST'])
def confirm_labeling():
    resp = {}
    first_check = labeler.confirm_labeling(g.graph, labeling)
    if not first_check[0]:
        resp["err"] = "Current labeling already invalid"
        resp["problems"] = first_check[1]
    else:
        resp = "Labeling is valid"
    return jsonify(resp)
