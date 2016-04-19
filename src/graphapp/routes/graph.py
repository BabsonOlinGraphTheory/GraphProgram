"""
Olin Graph Program Spring 2016
Authors: Josh Langowitz
Python 3

This module contains the persistent graph object and the Flask graph Blueprint.
"""
#Flask imports
from flask import Blueprint, request, jsonify

# Graphlib imports
from graphlib.graph import Graph
from graphlib.labeling import Labeling

# Graphapp imports
import graphapp.routes.labeling as l

# EXPORTS:
graph = Graph()
graph_blueprint = Blueprint("graph", __name__)

###############################################################################

# ROUTES:
@graph_blueprint.route("/new", methods=['POST'])
def new():
    global graph;
    data = request.get_json()
    print(data)
    adj = [set(l) for l in data["adj"]]
    graph = Graph(adj)
    print(graph.adjacency_list)
    l.labeling.labels = data["labeling"]
    print(l.labeling.labels)
    return "new graph created"

@graph_blueprint.route("/new/from_adjacency_matrix", methods=['POST'])
def new_from_adjacency_matrix():
    global graph;
    data = request.get_json()
    print(data)
    graph = Graph.new_from_adjacency_matrix(data["adj"])
    l.labeling.labels = data["labeling"]
    return "new graph created"

@graph_blueprint.route("/new/grid", methods=['POST'])
def new_grid():
    global graph;
    graph = Graph.new_grid(request.form["r"], request.form["c"], request.form["wrap"])
    l.labeling.labels = [None] * graph.num_verts()
    return "new graph created"

@graph_blueprint.route("/new/cycle", methods=['POST'])
def new_cycle():
    global graph;
    graph = Graph.new_cycle(request.form["v"])
    l.labeling.labels = [None] * graph.num_verts()
    return "new graph created"

@graph_blueprint.route("/vertex/add", methods=['POST'])
def add_vertex():
    graph.add_vertex()
    print(l.labeling)
    l.labeling.add_vertex()
    print(graph.adjacency_list)
    return "vertex added"

@graph_blueprint.route("/edge/add", methods=['POST'])
def add_edge():
    graph.add_edge(int(request.form["v1"]), int(request.form["v2"]))
    return "edge added"

@graph_blueprint.route("/vertex/remove", methods=['POST'])
def remove_vertex():
    graph.remove_vertex(int(request.form["v"]))
    l.labeling.remove_vertex(int(request.form["v"]))
    return "vertex removed"

@graph_blueprint.route("/edge/remove", methods=['POST'])
def remove_edge():
    graph.remove_edge(int(request.form["v1"]), int(request.form["v2"]))
    return "edge removed"

@graph_blueprint.route("/delete", methods=['POST'])
def delete():
    data = request.get_json()
    verts = data["vs"]
    edges = data["es"]
    print(verts)
    print(edges)
    print(graph.adjacency_list)
    for edge in edges:
        graph.remove_edge(edge["v1"], edge["v2"]);
    for vert in verts:
        graph.remove_vertex(vert)
        l.labeling.remove_vertex(vert)
    print(graph.adjacency_list)
    return "vertices and edges deleted"

@graph_blueprint.route("/connect", methods=['POST'])
def connect_vertices():
    graph.connect(request.form["vs"])
    return "vertices connected"

@graph_blueprint.route("/adj_mat", methods=['GET'])
def get_adjacency_matrix():
    return jsonify(graph.as_adjacency_matrix())
