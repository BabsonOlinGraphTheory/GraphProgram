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
# print(C_5.as_adjacency_matrix())
# print(C_5.adjacency_list())
C_5_also = Graph.new_from_adjacency_matrix(C_5.as_adjacency_matrix())
print(C_5_also.adjacency_list())
C_5.add_vertex()
C_5.add_edge(0,5)
C_5.add_edge(1,5)
C_5.add_edge(2,5)
C_5.add_edge(3,5)
C_5.add_edge(4,5)
print(C_5.adjacency_list())
C_5_directly = Graph.new_cycle(5)
print(C_5_directly.adjacency_list())
print(C_5.is_regular())
print(C_5_also.is_regular())
print(C_5.degrees())
C_5_tensor_prod = C_5_also.tensor_product(C_5_directly)
print(C_5_tensor_prod.adjacency_list())
C_5_cartesian_prod = C_5_also.cartesian_product(C_5_directly)
print(C_5_cartesian_prod.adjacency_list())
C_5_strong_prod = C_5_also.strong_product(C_5_directly)
print(C_5_strong_prod.adjacency_list())
print(C_5.shortest_path_matrix()) #Will need to look at this
grid_2_3 = Graph.new_grid(2,3,None)
print(grid_2_3.adjacency_list())
cylinder_2_3 = Graph.new_grid(2,3,"cylindrical")
print(cylinder_2_3.adjacency_list())
toroid_3_3 = Graph.new_grid(3,3,"toroidal")
print(toroid_3_3.adjacency_list())