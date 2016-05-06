"""
Olin Graph Program Fall 2014
Authors: Josh Langowitz
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
        Creates a new labeling

        labels - list of labels
        """
        self._labels = labels

    @property
    def labels(self):
        return self._labels
    
    @labels.setter
    def labels(self, labels):
        self._labels = labels

    def set_label(self, v, label):
        """
        Sets a specific label

        v     - vertex to label
        label - label to use
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
        Removes a label from the label list for the deletion of a vertex

        v - vertex to remove
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