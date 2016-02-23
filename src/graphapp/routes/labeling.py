"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent labeling object and the Flask labeling Blueprint.
"""
#Flask imports
from flask import Blueprint

# Graphlib imports
from graphlib.labeling import Labeling

# EXPORTS:
labeling = Labeling()
labeling_blueprint = Blueprint("labeling", __name__)

###############################################################################


