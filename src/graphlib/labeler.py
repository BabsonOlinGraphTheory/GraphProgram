"""
Olin Graph Program Fall 2014
Authors: Josh Langowitz
Python 3
"""
from graphlib.labeling import Labeling
from copy import deepcopy, copy
from abc import ABCMeta, abstractmethod

class Labeler(metaclass=ABCMeta):
    """
    Parent class for labelers with different constraints. Abstract base class, all labelers inherit from this.
    All subclasses MUST implement confirm_labeling_impl and complete_labeling_impl as private methods.

    CLASS METHODS:

    ATTRIBUTES:

    OBJECT METHODS:

    Concrete, Public:
        complete_labeling      - get a valid labeling of a graph
        confirm_labeling       - check to see if a labeling of a graph is valid

    Abstract, Private:
        complete_labeling_impl - called by complete_labeling
        confirm_labeling_impl  - called by confirm_labeling

    """

    # OBJECT METHODS:
    def complete_labeling(self, g, current_labeling, min_label, max_label):
        """
        Completes a labeling of a graph with the lowest possible highest label using this labeler.

        g                - graph to label
        current_labeling - labeling of g, or None
        min_label        - known lower bound (Takes longer if this is low, may not find lambda if this is too high)
        max_label        - known upper bound (May not find a labeling if this is low, should not matter if this is high)

        RETURNS: A labeling of the graph
        """
        # For convenience, allow passing in None as a labeling instead of a Labeling containing all Nones.
        if not current_labeling:
            current_labeling = Labeling([None] * g.num_verts())

        # Check the current labeling so we don't waste time looking for a labeling that isn't possible.
        if not self.confirm_labeling(g, current_labeling)[0]:
            raise(Exception("There is an error in your current labeling somewhere.")) #TODO: Find the error for them

        # Loop through all possible lambdas and try to find a valid labeling for that lambda 
        for val in range(min_label, max_label+1):
            potential_labeling = self.complete_labeling_impl(g.distance_matrix(), deepcopy(current_labeling), val)
            if potential_labeling:
                return potential_labeling
        raise(Exception("We could not find a valid labeling for this graph with your constraints. Check your bounds for min and max labels."))

    def confirm_labeling(self, g, current_labeling):
        """
        Checks if a labeling or partial labeling is valid but does not complete it. 
        Use this for checking labelings once, rather than to evaluate possible labelings inside a labeling method.

        g                - graph to check against
        current_labeling - labeling to check

        RETURNS: Whether the labeling is a valid labeling of the graph for this labeler.
        """
        return self.confirm_labeling_impl(g.distance_matrix(), deepcopy(current_labeling))

    @abstractmethod
    def confirm_labeling_impl(self, dist_mat, l):
        """
        Checks to see if the labeling is a valid labeling of the graph.

        dist_mat      - distance matrix of the graph to check the labeling agaisnt
        l             - labeling to check

        """
        raise(NotImplementedError("Subclasses must override confirm_labeling_impl"))

    @abstractmethod
    def complete_labeling_impl(self, dist_mat, current_labeling, max_label):
        """
        Tries to find a valid labeling of g with the highest label being max_label, given the current labeling.
        Not guaranteed to provide the most efficient labeling, if you are looking for that you will
        need to step down the max_label until this does not find a labeling.

        dist_mat         - distance matrix of the graph to check the labeling agaisnt
        current_labeling - labeling so far
        max_label        - highest label to allow
        """
        raise(NotImplementedError("Subclasses must override complete_labeling_impl"))

class LPolynomialLabeler(Labeler):
    """
    Labeler class for L(x_1, x_2, ..., x_n) labelings of graphs

    CLASS METHODS:

    Constructors:
        __init__

    ATTRIBUTES:

    Properties:
        constraints - tuple containing m and n

    OBJECT METHODS:

    Public:
        complete_labeling

    Private:
        confirm_labeling_impl
        check_label
        complete_labeling_impl
    """

    # CLASS METHODS
    def __init__(self, constraints=(2,1), holes='allowed'):
        self._constraints = constraints
        self.holes = holes

    #Properties
    @property
    def constraints(self):
        return self._constraints
    
    @constraints.setter
    def constraints(self, constraints):
        self._constraints = constraints

    # OBJECT METHODS
    def confirm_labeling_impl(self, dist_mat, l):
        """
        Checks to see if the labeling is a valid labeling of the graph.

        dist_mat      - distance matrix of the graph to check the labeling agaisnt
        l             - labeling to check

        """
        constraints = self.constraints
        labels = l.labels
        num_verts = len(labels)
        for i in range(num_verts - 1):
            for j in range(i+1, num_verts):
                if labels[i] != None and labels[j] != None:
                    if dist_mat[i][j] > 0 and dist_mat[i][j] <= len(constraints):
                        diff = abs(labels[i] - labels[j])
                        if diff < constraints[dist_mat[i][j]-1]:
                            return (False, (i,j))
        return (True, None)

    def check_label(self, dist_mat, l, v):
        """
        Checks to see if a single label in the labling is valid

        dist_mat - distance matrix of the graph to check the labeling agaisnt
        l        - labeling to check
        v        - vertex to check

        """
        constraints = self.constraints
        labels = l.labels
        num_verts = len(labels)
        for i in range(num_verts):
            if labels[i] != None and labels[v] != None:
                if dist_mat[i][v] > 0 and dist_mat[i][v] <= len(constraints):
                    diff = abs(labels[i] - labels[v])
                    if diff < constraints[dist_mat[i][v]-1]:
                        return False
        return True

    def complete_labeling_impl(self, dist_mat, current_labeling, max_label):
        """
        Tries to find a valid labeling of g with the highest label being max_label, given the current labeling.
        Not guaranteed to provide the most efficient labeling, if you are looking for that you will
        need to step down the max_label until this does not find a labeling.

        dist_mat         - distance matrix of the graph to check the labeling agaisnt
        current_labeling - labeling so far
        max_label        - highest label to allow
        """
        potential_labels = range(max_label+1)
        labels = current_labeling.labels
        vertex_to_label = 0
        # Find the first label that is None. If there isn't one, we are done labeling, 
        # so check the labeling and return it if it works, False otherwise.
        try:
            vertex_to_label = labels.index(None)
        except:
            if self.confirm_labeling_impl(dist_mat, current_labeling)[0]:
                return current_labeling
            else:
                return False

        # Guess the label at the first None position, trying each label less than the max, 
        # and then try to label the rest of the graph based on that guess, returning the first one that works
        for label in potential_labels:
            labels[vertex_to_label] = label
            current_labeling = Labeling(labels)
            if self.check_label(dist_mat, current_labeling, vertex_to_label):
                potential_labeling = self.complete_labeling_impl(dist_mat, Labeling(copy(labels)), max_label)
                if potential_labeling:
                    return potential_labeling
        return False
