"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""
from labeling import Labeling
from copy import deepcopy, copy

class Labeler:
    """
    Parent class for labelers with different constraints. Abstract class, all labelers inherit from this.

    CLASS METHODS:

    ATTRIBUTES:

    OBJECT METHODS:
        label
        check_labeling
    """

    # OBJECT METHODS:
    def label(self, G):
        """
        Labels a graph

        G            - a Graph object to label
        constraints - constraints for the labeling
        """
        raise("Abstract class, don't use this!")

    def check_labeling(self, G, L):
        """
        Checks to see that l is a correct labeling of G

        G            - a Graph object
        L            - a Labeling object
        """
        raise("Abstract class, don't use this!")

class LMNLabeler(Labeler):
    """
    Labeler class for L(m,n) labelings of graphs with and without holes

    CLASS METHODS:

    Constructors:
        __init__

    ATTRIBUTES:
        constraints - tuple containing m and n
        holes_mode  - enum indicating how to handle holes in labelings, can be 'allow', 'none', or 'minimize'

    OBJECT METHODS:

    Public:
        label
        check_labeling
        finish_labeling
        constraints

    Private:
        # All the k_labeling and helper stuff?

    """

    # CLASS METHODS
    def __init__(self, constraints, holes_mode):
        self.constraint_values= constraints
        self.holes_mode = holes_mode

    def constraints(self, *constraints):
        """
        Getter/Setter for constraints atribute
        """
        if constraints:
            self.constraint_values= constraints[0]
        return self.constraint_values

    # OBJECT METHODS
    def check_labeling(self, g, l):
        """
        Checks to see if l, a labeling object, is a valid labeling of g, a graph object.
        """
        (m,n) = self.constraints()
        labels = l.labels()
        num_verts = g.num_verts()
        dist_mat = g.distance_matrix()
        for i in range(num_verts - 1):
            for j in range(i+1, num_verts):
                if labels[i] != None and labels[j] != None:
                    diff = abs(labels[i] - labels[j])
                    if dist_mat[i][j] == 2:
                        if diff < n:
                            return False
                    if dist_mat[i][j] == 1:
                        if diff < m:
                            return False
        return True

    def check_label(self, g, dist_mat, l, v):
        """
        Checks to see if vertex v in g is validly labelled in labeling l
        """
        (m,n) = self.constraints()
        labels = l.labels()
        num_verts = g.num_verts()
        # dist_mat = g.distance_matrix()
        for i in range(num_verts):
            if labels[i] != None and labels[v] != None:
                diff = abs(labels[i] - labels[v])
                if dist_mat[i][v] == 2:
                    if diff < n:
                        return False
                if dist_mat[i][v] == 1:
                    if diff < m:
                        return False
        return True

    def complete_labeling(self, g, current_labeling, min_lambda, max_lambda):
        """
        Returns a valid labeling of g, a graph object, 
        pursuant to the labels already defined in current_labeling, a labeling object.
        min_lambda and max_lambda are the minimum and maximum lambdas of the graph.
        """
        if not current_labeling:
            current_labeling = Labeling([None] * g.num_verts())
        for lam in range(min_lambda, max_lambda+1):
            print(lam)
            potential_labeling = self.try_labeling(g, g.distance_matrix(), deepcopy(current_labeling), lam)
            if potential_labeling:
                return potential_labeling
        raise(Exception("Something went horribly wrong and we couldn't label this"))

    def try_labeling(self, g, dist_mat, current_labeling, max_label):
        """
        Tries to find a valid labeling of g with the highest label being max_label, given the current labeling.
        """
        potential_labels = range(max_label+1)
        labels = current_labeling.labels()
        try:
            current_label = labels.index(None)
            # print(current_label)
            for label in potential_labels:
                labels[current_label] = label
                # print(labels)
                current_labeling = Labeling(labels)
                if self.check_label(g, dist_mat, current_labeling, current_label):
                    # print(current_labeling.labels())
                    potential_labeling = self.try_labeling(g, dist_mat, Labeling(copy(labels)), max_label)
                    # print(potential_labeling.labels())
                    if potential_labeling and self.check_labeling(g, potential_labeling):
                        return potential_labeling
                # else:
                #     print(current_labeling.labels(), " was not valid")
            return False
        except:
            if self.check_labeling(g, current_labeling):
                return current_labeling
            else:
                return False


# # Works with reals.
# # a simple, no frills algorithm for automatically generating a smallest span labelling
#     def auto_label(self, graph, minmaxlabel):
         
#         if check_labeling(graph,self.constraints) != True:
#             return False
             
#         reals = 0
#         for constraint in self.constraints:
#             if type(constraint) == type(Decimal(0)):
#                 reals = 1
#                 break
#         for v in graph.verts:
#             if type(v.label) == type(Decimal(0)):
#                 reals = 1
#                 break
     
#         if self.holes_mode == "allow":
#     #        print "holes allowed"
#             final_check = holes_allowed
#         elif self.holes_mode == "none":
#     #        print "no holes allowed"
#             if reals == 1:
#                 return "RealError"
#             final_check = no_holes_allowed
#         elif self.holes_mode == "minimize":
#             if reals == 1:
#                 return "RealError"
#     #        print "minimize holes"
#             final_check = minimize_holes
#         else: # # default to holes allowed # # TODO: There is an error if you get this far!!!!
#             final_check = holes_allowed
     
#         size = len(graph.verts)
#         spm = shortestpathmatrix(graph.verts,graph.edges)
#         labs = labels(graph.verts)
#     #    maxdist = len(self.constraints)
#         maxlabel = minmaxlabel
#         # TODO: calculate lower bound of labeling, and test to see if it is better than this person's guess--this may eliminate really long wait
#         # TODO: for reals, change from index to actual number
         
#         initvertex = 0
#         # TODO: is there an optimum place to start?
         
     
#         memory = [None] # memory is a list so that changes made to it's contents will carry out of the methods
     
#         # There was a sketchy error happening if you don't explicitly pass "set=[]".  It just builds the dsets together from each auto-labeling...
         
#         d_set = build_d_set(self.constraints, len(graph.verts), setlist = [])
#         d_set=list(d_set)
#         d_set.sort()
#         print("d_set:", d_set)
#         # TODO: there's probably a simple way to combine the next two blocks of code.   
#         # If the initial vertex is precolored, this doesn't overwrite it
#         if labs[initvertex] != 'NULL':
#             while 1:
#                 res = try_label(spm, initvertex, labs[initvertex], maxlabel, labs, self.constraints, final_check, d_set, memory)
#                 if res != False:
#                     return res
#                 if self.holes_mode == "minimize" and memory[0] != None:
#         #            print memory[0][1]
#                     return memory[0][1]  # when minimizing
                 
#                 if maxlabel > len(d_set): 
#                     print("no labeling of the given type can be found.")
#                     raise("hell") # this means no labeling of the given type can be found.
#                 maxlabel += 1
#         # Only executes if the first label is not pre-colored.
#         while 1:
#     #        for label in range(int(ceil(maxlabel/2.))): # only need to try first half of the colors; second half is equivilent. if not prelabeled
#             for label in d_set[0:maxlabel+1]:
#                # what if initlabel was already labelled??  I think this breaks...
#                res = try_label(spm, initvertex, label, maxlabel, labs, self.constraints, final_check, d_set, memory)
#                print(res)
#                if res != False:
#                    return res
#             if self.holes_mode == "minimize" and memory[0] != None:
#     #            print memory[0][1]
#                 return memory[0][1]  # when minimizing
#             maxlabel += 1
#             if maxlabel > len(d_set):
#                 print("no labeling of the given type can be found.")
#                 raise("hell")
#                 raise("hell")
#                 raise("hell")
     
#     # Works with reals
#     # doesn't check for holes
#     def holes_allowed(labels, maxlabel, memory):
#     #    print "holes"
#         return labels
     
#     # Fundamentally flawed for reals; can't have holes/nonholes with reals.
#     # checks for holes, continues if holes are present
#     def no_holes_allowed(labels, maxlabel, memory):
#     #    print "noholes"
#         labels_used = [False] * (maxlabel + 1)
#         for entry in labels:
#             labels_used[entry] = True
#         full = True
#         index = 0
#         while full and index < maxlabel + 1:
#             full = full and labels_used[index]
#             index += 1
#         # TODO: simplify calculation of 'full' by just multiplying all indices, or checking if there is a zero, perhaps through a min(list) function?
#         if full:
#             return labels
#         else:
#             return False
     
#     # Fundamentally flawed for reals; can't have holes/nonholes with reals.
#     # looks for minimal holes
#     def minimize_holes(labels, maxlabel, memory):
#     #    print "minholes"
#         labels_used = [0] * (maxlabel + 1)
#         for entry in labels:
#             labels_used[entry] = 1
#         number_of_labels = sum(labels_used)
#     #    print number_of_labels
#         if number_of_labels == maxlabel + 1:
#             return labels
#         else:
#             if memory[0] == None or number_of_labels > memory[0][0]: # Shouldn't we be checking number of holes? (actually, this works, because it's minimum number of holes for a given maxlabel, but it's unclear)
#                 memory[0] = [number_of_labels,deepcopy(labels)]
#     #            print memory[0]
#             return False

#     # should work with reals
#     def try_label (spm, vertex, label, maxlabel, labels, constraints, final_check, d_set, memory = [None]):
#         #return [i for i in xrange(len(labels))]
#         #if vertex <= 3:
#         #  bar = "-"*vertex
#         #  print bar + str(color)
#         #yay for verbose output! Make sure not freezing with above code
     
#         # if pre-colored, then called with this as label, so we are not ignoring it.
#         labels[vertex] = label
#         if not check_vertex_labeling(spm[vertex], vertex, labels, constraints): # only need to pass check_labeling the current row of the SPM.
#             return False
     
#         # if we're on the last vertex, then check for holes if we are looking for a no-hole coloring
#         if (len(labels)-1 == vertex):
#             return final_check(labels, maxlabel, memory)
     
#         if labels[vertex+1] != 'NULL':
             
#             if try_label (spm, vertex+1, labels[vertex+1], maxlabel, labels, constraints, final_check, d_set, memory) != False:
#                 return labels
     
#         else:
#             for l in d_set[0:maxlabel+1]: # This is probably not correct if not using L(2,1) labeling because d_set may not be consecutive
#                 #for example, is d_set is [0, 1,3,4], max label of two, can't try to use three.
#     #        for l in range(maxlabel+1):   # TODO: improve efficiency here by selecting which colors we can use?  or only useful for going through list in right order?  won't speed up that much...
#                 if try_label(spm, vertex+1, l, maxlabel, labels, constraints, final_check, d_set, memory) != False:
#                     return labels
#             labels[vertex+1] = 'NULL' # reset vertex labeling so that it is not triggered as a pre-configured one next time through the algorithm
     
#         return False
     
#     # Works with reals
#     # Creates a matrix with vertices vs. vertices where the intersection an vertex x and vertex y is the shortest path from x to y.
#     # Completes this via a Breadth First Search to find paths for each vertex
#     def shortestpathmatrix(verts,edges):
#         adj = adjacencymatrix(verts,edges)
#     #    verts = self.graph.get_vertices()
#         size = len(verts)
#         for vert in range(size):
#             i = 2
#             A = [vert]
#             B = list(range(size))
#             B.remove(vert)
#             A = neighbors(adj,A,B)
#             for a in A:
#                 B.remove(a)
#             while B != [] and A != []:
#                 A = neighbors(adj,A,B)
#                 for a in A:
#                     adj[vert][a] = i
#                     adj[a][vert] = i
#                     B.remove(a)
#                 if A == []:
#                     for b in B:
#                         adj[vert][b] = -1
#                         adj[b][vert] = -1
#                 i=i+1
#         return adj

#     # Works with reals
#     # Creates a list with the labels of all vertices
#     def labels(verts):
#         return [vert.label for vert in verts]

#     # Works with reals
#     def build_d_set(constraints, numverts, i=0, setlist=[], addthis=0):
#         # I believe this creates a listing of all possible labels that could ever be needed for a graph with numvert verrtices
#         myset=set(setlist)
#         if i < len(constraints)-1:
#             for a in range(numverts):
#                 myset = build_d_set(constraints, numverts, i+1, myset, addthis+a*constraints[i])
#         else:
#             for a in range(numverts):
#                 myset.add(a*constraints[i]+addthis)
#                 print("a",a,"constraints", constraints,"i",i,"addthis", addthis)
#                 print(a*constraints[i]+addthis)
#         return myset

#     # Works with reals
#     # Takes in an adjacency matrix and a list "A" and "B" of vertices; returns a list of vertices in B that are adjacent to some vertex in A.
#     def neighbors(adj,A,B):
#         retlist = []
#         for b in B:
#             nlist = adj[b]
#             size = len(nlist)
#             for i in range(size):
#                 if nlist[i] == 1 and i in A:
#                     retlist.append(b)
#                     break
#         return retlist

#     # Works with reals
#     # Checks the current labeling according to the labeling constraints
#     def check_labeling(graph,constraints):
#         size = len(graph.verts)
#         spm = shortestpathmatrix(graph.verts,graph.edges)
#         cols = labels(verts)
#         maxdist = len(constraints)
     
#         #checks vertices using the shortest path matrix
#         for i in range(size-1):  # no need to check last vertex, because have checked all other against it.
#             for j in range(i+1,size):  # will have covered interaction of all vertices before this one with itself already
#                 dist = spm[i][j]
#                 if 0 < dist <= maxdist and cols[i] != 'NULL' and cols[j] != 'NULL':
#                     # only runs if labeling constraints are concerned with this short of path
#                     # and if both vertices are labelled.
#                     # finally, if dist < 0, then vertices are disconnected
#                     coldist = abs(cols[i]-cols[j])
#                     if coldist < constraints[dist-1]: #checks the coloring constraints to make sure it works
#                         return [False,(i,j)]
#                         #TODO: change this to throwing error and catching?
     
#         return True
