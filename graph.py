"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""
from graphmath import matrix_addition, identity

class Graph:
    """
    Model for storing a graph and performing graph operations

    CLASS METHODS:

    Constructors:
        __init__                  - new graph from adj list
        new_from_adjacency_matrix - new graph from adj matrix instead of list
        new_peterson              - new peterson graph
        new_star                  - new star graph
        new_cycle                 - new cycle
        new_grid                  - new rectangular grid
        new_mobius                - new moebius graph
        new_triangle_grid         - new triangular grid
        new_hex_grid              - new hexagonal grid
        new_partite               - new complete partite graph

    ATTRIBUTES:
        adj                       - adjacency list of vertices

    OBJECT METHODS:
        adjacency_list            - getter and setter for adj list attribute of a graph
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

    def new_from_adjacency_matrix(cls, m):
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
        cls.__init__(adj)

    def new_peterson(cls, v, l):
        """
        Creates a peterson graph with v vertices per layer and l layers
        """
        pass

    def new_cycle(cls, v, l):
        """
        Creates a cycle graph with v vertices per layer and l layers
        """
        pass

    def new_star(cls, v, skip):
        """
        Creates a star graph with v vertices per cycle and skipping skip vertices for cross connections
        """
        pass

    def new_grid(cls, r, c, wrap):
        """
        Creates a grid graph with r rows and c columns, with wrapping defined by wrap
        """
        pass

    def new_triangle_grid(cls, r, c, wrap):
        """
        Creates a triangle grid graph with r rows and c columns, with wrapping defined by wrap
        """
        pass

    def new_hex_grid(cls, r, c, wrap):
        """
        Creates a hex grid graph with r rows and c columns, with wrapping defined by wrap
        """
        pass

    def new_partite(cls, sizes):
        """
        Creates a complete partite graph with partition sizes according to sizes
        """
        pass

    # OBJECT METHODS
    def adjacency_list(self, adj):
        """
        Returns a representation of the graph as an adjacency list
        """
        if adj:
            self.adj = adj
        return self.adj

    def as_adjacency_matrix(self):
        """
        Returns a representation of the graph as an adjacency matrix
        """
        pass

    def add_vertex(self):
        """
        Adds a new vertex to the graph
        """
        adj = self.adjacency_list()
        adj.append([])
        self.adjacency_list(adj)

    def add_edge(self, v, w):
        """
        Adds a new edge from v to w to the graph
        """
        adj = self.adjacency_list()
        adj[v].append(w)
        adj[w].append(v)
        self.adjacency_list(adj)

    def is_regular(self):
        """
        Returns True if graph is regular, False otherwise
        """
        degrees = self.degrees()
        for i in range(1, len(degrees)):
            if degrees[i] != degrees[i-1]:
                return False
        return True

    def tensor_product(self, other):
        """
        Return the graph object representing the tensor product of graphs self and other
        """
        adj1 = self.as_adjacency_matrix()
        adj2 = other.as_adjacency_matrix()
        m=len(adj1)
        n=len(adj1[0])
        p=len(adj2)
        q=len(adj2[0])
        resadj=[]
        for i in range(m*p):
            resadj.append([None]*(n*q))
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    for l in range(q):
                        resadj[i*p+k][j*q+l]=adj1[i][j]*adj2[k][l]
        return type(self).new_from_adjacency_matrix(resadj)

    def cartesian_product(self, other):
        """
        Return the graph object representing the cartesian product of graphs self and other
        """
        pass

    def strong_product(self,other):
        """
        Return the graph object representing the strong product of graphs self and other
        """
        return matrix_addition(cartesian_product(self,other),tensor_product(self,other))

    def shortest_path_matrix(self):
        """
        Returns a matrix containing in the (i,j)th entry 
        the shortest path from vertex i to vertex j, using a Breadth First Search.
        """
        adj = self.as_adjacency_matrix()
        size = len(verts)
        for vert in range(size):
            i = 2
            A = [vert]
            B = list(range(size))
            B.remove(vert)
            A = neighbors(adj,A,B)
            for a in A:
                B.remove(a)
            while B != [] and A != []:
                A = neighbors(adj,A,B)
                for a in A:
                    adj[vert][a] = i
                    adj[a][vert] = i
                    B.remove(a)
                if A == []:
                    for b in B:
                        adj[vert][b] = -1
                        adj[b][vert] = -1
                i=i+1
        return adj

    def distance_matrix(self):
        """
        Returns a matrix containing in the (i,j)th entry 
        the distance of the shortest path from vertex i to vertex j.
        """
        spm = self.shortest_path_matrix()
        return [[len(path) for path in t] for t in spm]

    def neighbors(self, A, B):
        """
        Returns the vertices in A that are adjacent to at least one vertex in B
        """
        retlist = []
        adj = self.as_adjacency_matrix()
        for b in B:
            nlist = adj[b]
            size = len(nlist)
            for i in range(size):
                if nlist[i] == 1 and i in A:
                    retlist.append(b)
                    break
        return retlist

    def degrees(self):
        """
        Returns a list of the degrees of vertices in self
        """
        return [len(adjlist) for adjlist in self.adjacency_list()]

