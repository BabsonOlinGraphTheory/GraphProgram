"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

class Graph:
    """
    Model for storing a graph and performing graph operations

    CLASS METHODS:

    Constructors:
        __init__                  - new graph from adj list
        new_from_adjacency_matrix - new graph from adj matrix instead of list
        new_peterson              - new peterson graph
        new_star                  - new star graph
        new_cycle                 - 
        new_grid                  - 
        new_mobius                - 
        new_triangle_grid         - 
        new_hex_grid              - 
        new_partite               - 

    OBJECT METHODS:
        get_adjacency_list        - returns adj list representation of a graph
        as_adjacency_matrix       - returns adj matrix representation of a graph
        is_regular                - checks if graph is regular
        tensor_product            - returns tensor product of two graphs
        cartesian_product         - returns cartesian product of two graphs
        strong_product            - returns strong product of two graphs
        shortest_path_matrix      - returns matrix of shortest paths between vertices
        distance_matrix           - returns matrix of distances between vertices
        neighbors                 - returns members of one list of vertices that are adjacent to any member of a second list of vertices
        degrees                   - returns a list of degrees of each vertex

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
        pass

    def as_adjacency_matrix(self):
        """
        Returns a representation of the graph as an adjacency matrix
        """
        pass

    def is_regular(self):
        """
        Returns true if graph is regular, false otherwise
        """
        pass

    def shortest_path_matrix(self):
        """
        Returns a matrix containing in the (i,j)th entry 
        the shortest path from vertex i to vertex j.
        """
        pass

class Labeling:
    """
    Model for storing labelings of a graph

    CLASS METHODS:

    Constructors:
        __init__ - creates a labeling from a list of labels

    OBJECT METHODS:
        labels   - getter/setter for labels attribute
    """
    def __init__(self, labels=[]):
        self.labels = labels

    def labels(self, labels):
        """
        Sets the labels attribute to labels if it exists, then returns the labels

        labels - list of new labelings or none
        """


        