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