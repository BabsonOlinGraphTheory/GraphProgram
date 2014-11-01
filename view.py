"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

class View:
    """
    View class for graphs.
    Contains vertices and edges which have positions in the GUI,
    and knows how to draw itself.
    """
    # CONSTRUCTORS:
    def __init__(self, vertices=[], edges=[]):
        """
        Creates a view of a graph with the given vertices and edges

        vertices - list of Vertex objects
        edges    - list of Edge objects
        """
        self.vertices = vertices
        self.edges = edges

    def draw(self):
        """
        Draws the graph
        """
        