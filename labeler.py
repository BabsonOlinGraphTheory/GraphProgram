"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

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

    def check_labeling(self, G, l):
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
        holes_mode  - enum indicating how to handle holes in labelings
        label_range - tuple containing min and max label

    OBJECT METHODS:

    Public:
        label
        check_labeling
        finish_labeling

    Private:
        # All the k_labeling and helper stuff?

    """
    def __init__(constraints,holes_mode,label_range):
        self.constraints = constraints
        self.holes_mode = holes_mode
        self.label_range = label_range

# Works with reals.
# a simple, no frills algorithm for automatically generating a smallest span labelling
    def auto_label(self, graph, minmaxlabel):
         
        if check_labeling(graph,self.constraints) != True:
            return False
             
        reals = 0
        for constraint in self.constraints:
            if type(constraint) == type(Decimal(0)):
                reals = 1
                break
        for v in graph.verts:
            if type(v.label) == type(Decimal(0)):
                reals = 1
                break
     
        if self.holes_mode == "allow":
    #        print "holes allowed"
            final_check = holes_allowed
        elif self.holes_mode == "none":
    #        print "no holes allowed"
            if reals == 1:
                return "RealError"
            final_check = no_holes_allowed
        elif self.holes_mode == "minimize":
            if reals == 1:
                return "RealError"
    #        print "minimize holes"
            final_check = minimize_holes
        else: # # default to holes allowed # # TODO: There is an error if you get this far!!!!
            final_check = holes_allowed
     
        size = len(graph.verts)
        spm = shortestpathmatrix(graph.verts,graph.edges)
        labs = labels(graph.verts)
    #    maxdist = len(self.constraints)
        maxlabel = minmaxlabel
        # TODO: calculate lower bound of labeling, and test to see if it is better than this person's guess--this may eliminate really long wait
        # TODO: for reals, change from index to actual number
         
        initvertex = 0
        # TODO: is there an optimum place to start?
         
     
        memory = [None] # memory is a list so that changes made to it's contents will carry out of the methods
     
        # There was a sketchy error happening if you don't explicitly pass "set=[]".  It just builds the dsets together from each auto-labeling...
         
        d_set = build_d_set(self.constraints, len(graph.verts), setlist = [])
        d_set=list(d_set)
        d_set.sort()
        print("d_set:", d_set)
        # TODO: there's probably a simple way to combine the next two blocks of code.   
        # If the initial vertex is precolored, this doesn't overwrite it
        if labs[initvertex] != 'NULL':
            while 1:
                res = try_label(spm, initvertex, labs[initvertex], maxlabel, labs, self.constraints, final_check, d_set, memory)
                if res != False:
                    return res
                if self.holes_mode == "minimize" and memory[0] != None:
        #            print memory[0][1]
                    return memory[0][1]  # when minimizing
                 
                if maxlabel > len(d_set): 
                    print("no labeling of the given type can be found.")
                    raise("hell") # this means no labeling of the given type can be found.
                maxlabel += 1
        # Only executes if the first label is not pre-colored.
        while 1:
    #        for label in range(int(ceil(maxlabel/2.))): # only need to try first half of the colors; second half is equivilent. if not prelabeled
            for label in d_set[0:maxlabel+1]:
               # what if initlabel was already labelled??  I think this breaks...
               res = try_label(spm, initvertex, label, maxlabel, labs, self.constraints, final_check, d_set, memory)
               print(res)
               if res != False:
                   return res
            if self.holes_mode == "minimize" and memory[0] != None:
    #            print memory[0][1]
                return memory[0][1]  # when minimizing
            maxlabel += 1
            if maxlabel > len(d_set):
                print("no labeling of the given type can be found.")
                raise("hell")
                raise("hell")
                raise("hell")
     
    # Works with reals
    # doesn't check for holes
    def holes_allowed(labels, maxlabel, memory):
    #    print "holes"
        return labels
     
    # Fundamentally flawed for reals; can't have holes/nonholes with reals.
    # checks for holes, continues if holes are present
    def no_holes_allowed(labels, maxlabel, memory):
    #    print "noholes"
        labels_used = [False] * (maxlabel + 1)
        for entry in labels:
            labels_used[entry] = True
        full = True
        index = 0
        while full and index < maxlabel + 1:
            full = full and labels_used[index]
            index += 1
        # TODO: simplify calculation of 'full' by just multiplying all indices, or checking if there is a zero, perhaps through a min(list) function?
        if full:
            return labels
        else:
            return False
     
    # Fundamentally flawed for reals; can't have holes/nonholes with reals.
    # looks for minimal holes
    def minimize_holes(labels, maxlabel, memory):
    #    print "minholes"
        labels_used = [0] * (maxlabel + 1)
        for entry in labels:
            labels_used[entry] = 1
        number_of_labels = sum(labels_used)
    #    print number_of_labels
        if number_of_labels == maxlabel + 1:
            return labels
        else:
            if memory[0] == None or number_of_labels > memory[0][0]: # Shouldn't we be checking number of holes? (actually, this works, because it's minimum number of holes for a given maxlabel, but it's unclear)
                memory[0] = [number_of_labels,deepcopy(labels)]
    #            print memory[0]
            return False
