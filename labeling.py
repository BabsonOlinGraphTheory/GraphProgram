"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

class Labeling:
    """
    Model for storing labelings of a graph

    CLASS METHODS:

    Constructors:
        __init__  - creates a labeling from a list of labels

    OBJECT METHODS:
        labels    - getter/setter for labels attribute
        max_label - returns maximum label used
        holes     - returns values that are holes in the labeling
        num_holes - returns the number of holes in the labeling
    """
    # CONSTRUCTORS
    def __init__(self, labels=[]):
        """
        Creates a new labeling with labels as its labels
        """
        self._labels = labels

    @property
    def labels(self):
        return self._labels
    
    @labels.setter
    def labels(self, labels):
        """
        Sets the labels attribute to labels if it exists, then returns the labels

        labels - list of new labelings or none
        """
        if labels:
            self._labels = labels[0]
        return self.labels 

    def set_label(self, v, label):
        """
        Sets the label at vertex v to label
        """
        labels = self.labels
        labels[v] = label
        self.labels = labels 

    def add_vertex(self):
        """
        Appends an empty label to the label list for a new vertex
        """
        labels = self.labels
        labels.append(None)
        self.labels = labels 

    def remove_vertex(self, v):
        """
        Removes the vth label from the label list for the deletion of a vertex
        """
        labels = self.labels
        labels.pop(v)
        self.labels = labels

    def max_label(self):
        """
        Returns the maximum label used
        """
        return max(self.labels)

    def holes(self):
        """
        Returns the holes in the labeling
        """
        return [i for i in range(self.max_label()) if i not in self.labels]