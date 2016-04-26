"""
Olin Graph Program Fall 2014
Authors: Josh Langowitz
Python 3
"""
from graphlib.graphmath import matrix_addition, identity, cartesian_product, tensor_product, strong_product

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

    Properties:
        adjacency_list            - adjacency list of vertices

    OBJECT METHODS:
        as_adjacency_matrix       - returns adj matrix representation of a graph
        is_regular                - checks if graph is regular
        tensor_product            - returns tensor product of two graphs
        cartesian_product         - returns cartesian product of two graphs
        strong_product            - returns strong product of two graphs
        shortest_path_matrix      - returns matrix of shortest paths between vertices TODO: make this do what it says!
        distance_matrix           - returns matrix of distances between vertices
        neighbors                 - returns members of one list of vertices that are adjacent to any member of a second list of vertices
        degrees                   - returns a list of degrees of each vertex
        remove_vertex             - removes a vertex
        add_vertex                - adds a vertex
        remove_edge               - removes a edge
        add_edge                  - adds a edge
        connect                   - connects a set of vertices
        num_verts                 - get number of vertices

    """

    # CONSTRUCTORS
    def __init__(self, adj=[]):
        """
        Creates a graph with the given adjacency list, if passed.

        adj - list of sets such that adj[i] contains a set of indices corresponding to vertices adjacent to i.
        """
        self._adjacency_list = adj

    @classmethod
    def new_from_adjacency_matrix(cls, m):
        """
        Creates a graph from the given adjacency matrix.

        m - adjacency matrix

        RETURNS: The created graph
        """
        adj = []
        for i in range(len(m)):
            adj.append(set())
            for j in range(len(m[i])):
                if m[i][j]:
                    adj[i].add(j)
        return cls(adj)

    #TODO: Implement or remove
    @classmethod
    def new_peterson(cls, v, l):
        """
        Creates a peterson graph

        v - vertices per layer
        l - layers
        
        RETURNS: The created graph
        """
        pass

    @classmethod
    def new_cycle(cls, v):
        """
        Creates a cycle graph

        v - number of vertices

        RETURNS: The created graph
        """
        adj = [{(i-1) % v, (i+1) % v} for i in range(v)]
        return cls(adj)

    #TODO: Implement or remove
    @classmethod
    def new_star(cls, v, skip):
        """
        Creates a star graph
        v    - vertices per cycle 
        skip - number of vertices skipped for cross connections

        RETURNS: The created graph
        """
        pass

    @classmethod
    def new_grid(cls, r, c, wrap):
        """
        Creates a grid graph 
        r    - number of rows
        c    - number of columns
        wrap - indicator of any grid wrapping

        RETURNS: The created graph
        """
        adj = []
        # Go through vertices one row at a time, so that moving right increments index by 1
        # and moving down increments index by c.
        for i in range(0,r*c,c):
            for j in range(c):
                connections = []
                connections.extend([vert for vert in [i+j-1, i+j+1] if i<=vert<i+c]) #add horizontal connections
                connections.extend([vert for vert in [i+j-c, i+j+c] if 0<=vert<r*c]) #add vertical connections
                adj.append(set(connections))
        if wrap == "cylindrical" or wrap == "toroidal":
            if c>2:
                for i in range(0, r*c, c):
                    j = i+c-1
                    adj[i].add(j)
                    adj[j].add(i)
        if wrap == "toroidal":
            if r>2:
                for i in range(c):
                    j = (r-1)*c + i
                    adj[i].add(j)
                    adj[j].add(i)
        return cls(adj)

    #TODO: Implement or remove
    @classmethod
    def new_triangle_grid(cls, r, c, wrap):
        """
        Creates a triangle grid graph
        r    - number of rows
        c    - number of columns
        wrap - indicator of any grid wrapping

        RETURNS: The created graph
        """
        pass

    #TODO: Implement or remove
    @classmethod
    def new_hex_grid(cls, r, c, wrap):
        """
        Creates a hex grid graph
        r    - number of rows
        c    - number of columns
        wrap - indicator of any grid wrapping

        RETURNS: The created graph
        """
        pass

    #TODO: Implement or remove
    @classmethod
    def new_partite(cls, sizes):
        """
        Creates a complete partite graph
        sizes - list containing partition sizes

        RETURNS: The created graph
        """
        pass

    # OBJECT METHODS

    @property
    def adjacency_list(self):
        """
        RETURNS: the graph's adjacency list
        """
        return self._adjacency_list

    @adjacency_list.setter
    def adjacency_list(self, adj):
        self._adjacency_list = adj
    
    def num_verts(self):
        """
        RETURNS: the number of vertices in the graph
        """
        return len(self.adjacency_list)

    def as_adjacency_matrix(self):
        """
        RETURNS: a representation of the graph as an adjacency matrix
        """
        adj = self.adjacency_list
        mat=[]
        for verts in adj:
            row = [0]*len(adj)
            for vert in verts:
                row[vert] = 1
            mat.append(row)
        return mat

    def remove_vertex(self, v):
        """
        Removes a vertex in the graph and all incident edges

        v - vertex to remove
        """
        # Pop the deleted vertex, remove all adjacencies to it in other vertices, 
        # then decrement adjacencies to higher index vertices
        adj = self.adjacency_list
        adj.pop(v)
        for vert in adj:
            if v in vert:
                vert.remove(v)
            decrements = set()
            for connection in vert:
                if connection > v:
                    decrements.add(connection)
            vert.difference_update(decrements)
            vert.update({decrement - 1 for decrement in decrements})
        self.adjacency_list = adj

    def remove_edge(self, v, w):
        """
        Removes an edge in the graph

        v - vertex incident to the edge
        w - other vertex incident to the edge
        """
        adj = self.adjacency_list
        adj[v].remove(w)
        adj[w].remove(v)
        self.adjacency_list = adj

    def add_vertex(self):
        """
        Adds a new, unconnected, vertex to the graph
        """
        adj = self.adjacency_list
        adj.append(set())
        self.adjacency_list = adj

    def add_edge(self, v, w):
        """
        Adds a new edge to the graph

        v - vertex incident to the edge
        w - other vertex incident to the edge
        """
        adj = self.adjacency_list
        adj[v].add(w) 
        adj[w].add(v) 
        self.adjacency_list = adj

    def connect(self, vs):
        """
        Adds edges between each pair of vertices

        vs - list of vertices to connect
        """
        adj = self.adjacency_list
        for v1 in vs:
            for v2 in vs:
                if v1 != v2:
                    adj[v1].add(v2)
        self.adjacency_list = adj

    def is_regular(self):
        """
        RETURNS: True if graph is regular, False otherwise
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
        resadj = tensor_product(adj1, adj2)
        return type(self).new_from_adjacency_matrix(resadj)

    def cartesian_product(self, other):
        """
        Return the graph object representing the cartesian product of graphs self and other
        """
        adj1 = self.as_adjacency_matrix()
        adj2 = other.as_adjacency_matrix()
        resadj = cartesian_product(adj1, adj2)
        return type(self).new_from_adjacency_matrix(resadj)

    def strong_product(self,other):
        """
        Return the graph object representing the strong product of graphs self and other
        """
        adj1 = self.as_adjacency_matrix()
        adj2 = other.as_adjacency_matrix()
        resadj = strong_product(adj1, adj2)
        return type(self).new_from_adjacency_matrix(resadj)

    def shortest_path_matrix(self): #This seems to give distances, not actual paths
        """
        RETURNS: a matrix containing in the (i,j)th entry 
        the distance from vertex i to vertex j.
        """
        adj = self.as_adjacency_matrix()
        size = len(adj)
        # BFS for shortest paths
        for vert in range(size):
            i = 2
            A = [vert]
            B = list(range(size))
            B.remove(vert)
            A = self.neighbors(A,B)
            for a in A:
                B.remove(a)
            while B != [] and A != []:
                A = self.neighbors(A,B)
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

    def distance_matrix(self): #Since spm gives distances not paths, this is probably redundant, leaving as alias for now.
        """
        RETURNS: a matrix containing in the (i,j)th entry 
        the distance of the shortest path from vertex i to vertex j.
        """
        spm = self.shortest_path_matrix()
        return spm

    def neighbors(self, A, B):
        """
        RETURNS: the vertices in A that are adjacent to at least one vertex in B
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
        RETURNS: a list of the degrees of vertices in self
        """
        return [len(adjlist) for adjlist in self.adjacency_list]

