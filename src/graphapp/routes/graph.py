"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent graph object and the Flask graph Blueprint.
"""
#Flask imports
from flask import Blueprint

# Graphlib imports
from graphlib.graph import Graph

# EXPORTS:
graph = Graph()
graph_blueprint = Blueprint("graph", __name__)

###############################################################################




