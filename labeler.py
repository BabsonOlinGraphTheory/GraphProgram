"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

class Labeler(object):
    """
    Parent class for labelers with different constraints

    """
    def __init__(self, arg):
        super(Labeler, self).__init__()
        self.arg = arg
        

def label(G, constraints):
    """
    Labels a graph, pursuant to constraints

    G            - a Graph object to label
    constraints - constraints for the labeling
    """

def check_labeling(G, l, constraints):
    """
    Checks to see that l is a correct labeling of G, pursuant to constraints

    G            - a Graph object to label
    l            - a potential labeling for G
    constraints - constraints for the labeling
    """