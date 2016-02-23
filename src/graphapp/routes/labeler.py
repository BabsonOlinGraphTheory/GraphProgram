"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent labeler object and the Flask labeler Blueprint.
"""
#Flask imports
from flask import Blueprint

# Graphlib imports
from graphlib.labeler import LPolynomialLabeler

# EXPORTS:
labeler = LPolynomialLabeler()
labeler_blueprint = Blueprint("labeler", __name__)

###############################################################################


