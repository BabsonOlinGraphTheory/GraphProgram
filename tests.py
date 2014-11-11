"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

from graph import *
from graphmath import *
from labeler import *
from labeling import *

C_5 = Graph([
    [1,4],
    [0,2],
    [1,3],
    [2,4],
    [0,3],
])
print(C_5.as_adjacency_matrix())
print(C_5.adjacency_list())