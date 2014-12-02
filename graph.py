"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""
from graphmath import matrix_addition, identity, cartesian_product, tensor_product, strong_product

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

    @classmethod
    def new_from_adjacency_matrix(cls, m):
        """
        Creates a graph from the given adjacency matrix.

        m - adjacency matrix
        """
        adj = []
        for i in range(len(m)):
            adj.append([])
            for j in range(len(m[i])):
                if m[i][j]:
                    adj[i].append(j)
        return cls(adj)

    @classmethod
    def new_peterson(cls, v, l):
        """
        Creates a peterson graph with v vertices per layer and l layers
        """
        pass

    @classmethod
    def new_cycle(cls, v):
        """
        Creates a cycle graph with v vertices
        """
        adj = [[(i-1) % v, (i+1) % v] for i in range(v)]
        return cls(adj)

    @classmethod
    def new_star(cls, v, skip):
        """
        Creates a star graph with v vertices per cycle and skipping skip vertices for cross connections
        """
        pass

    @classmethod
    def new_grid(cls, r, c, wrap):
        """
        Creates a grid graph with r rows and c columns, with wrapping defined by wrap
        """
        adj = []
        # Go through vertices one row at a time, so that moving right increments index by 1
        # and moving down increments index by c.
        for i in range(0,r*c,c):
            for j in range(c):
                connections = []
                connections.extend([vert for vert in [i+j-1, i+j+1] if i<=vert<i+c]) #add horizontal connections
                connections.extend([vert for vert in [i+j-c, i+j+c] if 0<=vert<r*c]) #add horizontal connections
                adj.append(connections)
        if wrap == "cylindrical" or wrap == "toroidal":
            if c>2:
                for i in range(0, r*c, c):
                    j = i+c-1
                    adj[i].append(j)
                    adj[j].append(i)
        if wrap == "toroidal":
            if r>2:
                for i in range(c):
                    j = (r-1)*c + i
                    adj[i].append(j)
                    adj[j].append(i)
        return cls(adj)

    @classmethod
    def new_triangle_grid(cls, r, c, wrap):
        """
        Creates a triangle grid graph with r rows and c columns, with wrapping defined by wrap
        """
        pass

    @classmethod
    def new_hex_grid(cls, r, c, wrap):
        """
        Creates a hex grid graph with r rows and c columns, with wrapping defined by wrap
        """
        pass

    @classmethod
    def new_partite(cls, sizes):
        """
        Creates a complete partite graph with partition sizes according to sizes
        """
        pass

    # OBJECT METHODS
    def num_verts(self):
        """
        Returns the number of vertices in self
        """
        return len(self.adj)

    def adjacency_list(self, *adj):
        """
        Getter/Setter for adj atribute
        """
        if adj:
            self.adj = adj[0]
        return self.adj

    def as_adjacency_matrix(self):
        """
        Returns a representation of the graph as an adjacency matrix
        """
        adj = self.adjacency_list()
        mat=[]
        for verts in adj:
            row = [0]*len(adj)
            for vert in verts:
                row[vert] = 1
            mat.append(row)
        return mat

    def remove_vertex(self, v):
        """
        Removes the vth vertex in the graph and all incident edges
        """
        # Pop the deleted vertex, remove all adjacencies to it in other vertices, 
        # then decrement adjacencies to higher index vertices
        adj = self.adjacency_list()
        adj.pop(v)
        for vert in adj:
            if v in vert:
                vert.remove(v)
            for connection in vert:
                if connection > v:
                    vert[vert.index(connection)] -= 1
        self.adjacency_list(adj)

    def remove_edge(self, v, w):
        """
        Removes the edge in the graph connecting vertices v and w
        """
        adj = self.adjacency_list()
        adj[v].remove(w)
        adj[w].remove(v)
        self.adjacency_list(adj)

    def add_vertex(self):
        """
        Adds a new vertex to the graph
        """
        adj = self.adjacency_list()
        adj.append([])
        self.adjacency_list(adj)

    # Deprecate this in favor of connect or leave for convenience? This is very slightly more efficient
    def add_edge(self, v, w):
        """
        Adds a new edge from v to w to the graph
        """
        adj = self.adjacency_list()
        if w not in adj[v]:
            adj[v].append(w) 
        if v not in adj[w]:
            adj[w].append(v) 
        self.adjacency_list(adj)

    def connect(self, vs):
        """
        Adds edges between each pair of vertices in vs
        """
        adj = self.adjacency_list()
        for v1 in vs:
            for v2 in vs:
                if v1 != v2 and v2 not in adj[v1]:
                    adj[v1].append(v2)

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
        Returns a matrix containing in the (i,j)th entry 
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
        Returns a matrix containing in the (i,j)th entry 
        the distance of the shortest path from vertex i to vertex j.
        """
        spm = self.shortest_path_matrix()
        return spm
        # return [[len(path) for path in t] for t in spm]

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

