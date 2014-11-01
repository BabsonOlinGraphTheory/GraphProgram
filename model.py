"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

class Graph:
    """
    Model for storing a graph

    CLASS METHODS:

    Constructors:

    OBJECT METHODS:

    """


    # CONSTRUCTORS
    def __init__(self, adj=[]):
        """
        Creates a graph with the given adjacency list, if passed.

        adj - list of lists such that adj[i] contains a list of indices corresponding to vertices adjacent to i.
        """
        self.adj = adj

    def new_from_adjacency_matrix(self, m):
        """
        Creates a graph from the given adjacency matrix.

        m - adjacency matrix
        """
        adj = []
        for i in xrange(len(m)):
            adj.append([])
            for j in xrange(len(m[i])):
                if m[i][j]:
                    adj[i].append(j)
        self.__init__(adj)

    # OBJECT METHODS
    def get_adjacency_list(self):
        """
        Returns a representation of the graph as an adjacency list
        """

    def as_adjacency_matrix(self):
        """
        Returns a representation of the graph as an adjacency matrix
        """


