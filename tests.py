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
# print(C_5_also.adjacency_list())
C_5.add_vertex()
C_5.add_edge(0,5)
C_5.add_edge(1,5)
C_5.add_edge(2,5)
C_5.add_edge(3,5)
C_5.add_edge(4,5)
# print(C_5.adjacency_list())
C_5_directly = Graph.new_cycle(5)
# print(C_5_directly.adjacency_list())
# print(C_5.is_regular())
# print(C_5_also.is_regular())
# print(C_5.degrees())
C_5_tensor_prod = C_5_also.tensor_product(C_5_directly)
# print(C_5_tensor_prod.adjacency_list())
C_5_cartesian_prod = C_5_also.cartesian_product(C_5_directly)
# print(C_5_cartesian_prod.adjacency_list())
C_5_strong_prod = C_5_also.strong_product(C_5_directly)
# print(C_5_strong_prod.adjacency_list())
# print(C_5.shortest_path_matrix()) #Will need to look at this
grid_2_3 = Graph.new_grid(2,3,None)
# print(grid_2_3.adjacency_list())
cylinder_2_3 = Graph.new_grid(2,3,"cylindrical")
# print(cylinder_2_3.adjacency_list())
toroid_3_3 = Graph.new_grid(3,3,"toroidal")
# print(toroid_3_3.adjacency_list())

labeler = LMNLabeler((2,1),"allowed")
C_5_labeling = Labeling([None]*C_5_also.num_verts())
# print(C_5_labeling.labels())
C_5_valid_labeling = labeler.complete_labeling(C_5_also, C_5_labeling, 3, 4)
print(C_5_valid_labeling.labels())
grid_2_3_valid_labeling = labeler.complete_labeling(grid_2_3, None, 4, 9)
print(grid_2_3_valid_labeling.labels())
cylinder_2_3_valid_labeling = labeler.complete_labeling(cylinder_2_3, None, 4, 9)
print(cylinder_2_3_valid_labeling.labels())
toroid_3_3_valid_labeling = labeler.complete_labeling(toroid_3_3, None, 5, 16)
print(toroid_3_3_valid_labeling.labels())

C_5_labeling.set_label(1,1)
print(C_5_labeling.labels())
print(labeler.complete_labeling(C_5_also, C_5_labeling, 3, 4).labels())
print(labeler.complete_labeling(Graph.new_cycle(13), None, 3, 4).labels())
print(labeler.complete_labeling(Graph.new_grid(13, 4, None), None, 4, 9).labels())
