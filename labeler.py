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
        complete_labeling
    """

    # OBJECT METHODS:
    def complete_labeling(self, g, current_labeling, min_label, max_label):
        """
        Returns a valid labeling of g, a graph object, 
        pursuant to the labels already defined in current_labeling, a labeling object.
        min_label and max_label are the minimum and maximum labels of the graph.
        """
        # For convenience, allow passing in None as a labeling instead of a Labeling containing all Nones.
        if not current_labeling:
            current_labeling = Labeling([None] * g.num_verts())

        # Check the current labeling so we don't waste time looking for a labeling that isn't possible.
        if not self.confirm_labeling(g, current_labeling):
            raise(Exception("There is an error in your current labeling somewhere.")) #TODO: Find the error for them

        # Loop through all possible lambdas and try to find a valid labeling for that lambda 
        for val in range(min_label, max_label+1):
            potential_labeling = self.try_labeling(g.distance_matrix(), deepcopy(current_labeling), val)
            if potential_labeling:
                return potential_labeling
        raise(Exception("We could not find a valid labeling for this graph with your constraints. Check your bounds for min and max labels."))

    def confirm_labeling(self, g, current_labeling):
        """
        Essentially a wrapper for check_labeling for the abstract class. 
        Use this for checking labelings once, rather than to evaluate possible labelings inside a labeling method.
        """
        return self.check_labeling(g.distance_matrix(), current_labeling)

class LPolynomialLabeler(Labeler):
    """
    Labeler class for L(x_1, x_2, ..., x_n) labelings of graphs with and without holes

    CLASS METHODS:

    Constructors:
        __init__

    ATTRIBUTES:
        constraint_values - tuple containing m and n
        holes  - enum indicating how to handle holes in labelings, can be 'allow', 'none', or 'minimize'

    OBJECT METHODS:

    Public:
        complete_labeling
        constraints
        holes_mode

    Private:
        check_labeling
        check_label
        try_labeling
    """

    # CLASS METHODS
    def __init__(self, constraints=(2,1), holes='allowed'):
        self.constraint_values = constraints
        self.holes = holes

    def constraints(self, *constraints):
        """
        Getter/Setter for constraint_values atribute
        """
        if constraints:
            self.constraint_values= constraints[0]
        return self.constraint_values

    def holes_mode(self, *holes_mode):
        """
        Getter/Setter for holes atribute
        """
        if holes_mode:
            self.holes= holes_mode[0]
        return self.holes

    # OBJECT METHODS
    def check_labeling(self, dist_mat, l):
        """
        Checks to see if l, a labeling object, is a valid labeling of a graph with distance matrix dist_mat.
        """
        constraints = self.constraints()
        labels = l.labels()
        num_verts = len(labels)
        for i in range(num_verts - 1):
            for j in range(i+1, num_verts):
                if labels[i] != None and labels[j] != None:
                    if dist_mat[i][j] > 0 and dist_mat[i][j] <= len(constraints):
                        diff = abs(labels[i] - labels[j])
                        if diff < constraints[dist_mat[i][j]-1]:
                            return False
        return True

    def check_label(self, dist_mat, l, v):
        """
        Checks to see if vertex v in a graph with distance matrix dist_mat is validly labelled in labeling l
        """
        constraints = self.constraints()
        labels = l.labels()
        num_verts = len(labels)
        for i in range(num_verts):
            if labels[i] != None and labels[v] != None:
                if dist_mat[i][v] > 0 and dist_mat[i][v] <= len(constraints):
                    diff = abs(labels[i] - labels[v])
                    if diff < constraints[dist_mat[i][v]-1]:
                        return False
        return True

    def try_labeling(self, dist_mat, current_labeling, max_label):
        """
        Tries to find a valid labeling of g with the highest label being max_label, given the current labeling.
        """
        potential_labels = range(max_label+1)
        labels = current_labeling.labels()
        vertex_to_label = 0
        # Find the first label that is None. If there isn't one, we are done labeling, 
        # so check the labeling and return it if it works, False otherwise.
        try:
            vertex_to_label = labels.index(None)
        except:
            if self.check_labeling(dist_mat, current_labeling):
                return current_labeling
            else:
                return False

        # Guess the label at the first None position, trying each label less than the max, 
        # and then try to label the rest of the graph based on that guess, returning the first one that works
        for label in potential_labels:
            labels[current_label] = label
            current_labeling = Labeling(labels)
            if self.check_label(dist_mat, current_labeling, current_label):
                potential_labeling = self.try_labeling(dist_mat, Labeling(copy(labels)), max_label)
                if potential_labeling:
                    return potential_labeling
        return False