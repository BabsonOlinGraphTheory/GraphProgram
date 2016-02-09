"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3

Run test with 'python -m unittest'
"""

# TODO: tests for graph products

from graph import *
from graphmath import *
from labeler import *
from labeling import *
import unittest

class TestGraphC5(unittest.TestCase):
    """
    Tests for graph model using cycles
    """

    def setUp(self):
        self.adj_list = [
            [1,4],
            [0,2],
            [1,3],
            [2,4],
            [0,3],
        ]
        self.adj_mat = [
            [0,1,0,0,1],
            [1,0,1,0,0],
            [0,1,0,1,0],
            [0,0,1,0,1],
            [1,0,0,1,0],
        ]
        self.spm = [
            [0,1,2,2,1],
            [1,0,1,2,2],
            [2,1,0,1,2],
            [2,2,1,0,1],
            [1,2,2,1,0],
        ]
        self.graph = Graph(self.adj_list)

    def test_adjacency_list(self):
        self.assertEqual(self.adj_list, self.graph.adjacency_list())
        self.assertEqual(self.adj_list, self.graph.adjacency_list(self.adj_list))

    def test_adjacency_matrix(self):
        self.assertEqual(self.graph.as_adjacency_matrix(), self.adj_mat)

    def test_add_vertex(self):
        self.adj_list.append([])
        self.graph.add_vertex()
        self.assertEqual(self.graph.adjacency_list(), self.adj_list)

    def test_add_edge(self):
        self.graph.add_edge(1,2)
        self.adj_list[1].append(2)
        self.adj_list[2].append(1)
        self.assertEqual(self.graph.adjacency_list(), self.adj_list)

    def test_new_cycle(self):
        self.assertEqual(self.graph.adjacency_list().sort(), Graph.new_cycle(5).adjacency_list().sort())

    def test_is_regular(self):
        self.assertTrue(self.graph.is_regular())
        self.graph.add_edge(1,2)
        self.assertFalse(self.graph.is_regular())

    def test_delete_vertex(self):
        self.graph.delete_vertex(2)
        self.adj_list = [
            [1,3],
            [0],
            [3],
            [0,2],
        ]
        self.assertEqual(self.graph.adjacency_list(), self.adj_list)

    def test_num_verts(self):
        self.assertEqual(self.graph.num_verts(), 5)

    def test_degrees(self):
        self.assertEqual(self.graph.degrees(), [2] * 5)

    def test_new_from_adjacency_matrix(self):
        self.assertEqual(Graph.new_from_adjacency_matrix(self.adj_mat).adjacency_list(), self.adj_list)

    def test_shortest_path_matrix(self):
        self.assertEqual(self.graph.shortest_path_matrix(), self.spm)

class TestLPolynomialLabeler(unittest.TestCase):
    """
    Tests for LPolynomialLabeler
    """
    pass #TODO: write these


# C_5 = Graph([
#     [1,4],
#     [0,2],
#     [1,3],
#     [2,4],
#     [0,3],
# ])
# # print(C_5.as_adjacency_matrix())
# # print(C_5.adjacency_list())
# C_5_also = Graph.new_from_adjacency_matrix(C_5.as_adjacency_matrix())
# # print(C_5_also.adjacency_list())
# C_5.add_vertex()
# C_5.add_edge(0,5)
# C_5.add_edge(1,5)
# C_5.add_edge(2,5)
# C_5.add_edge(3,5)
# C_5.add_edge(4,5)
# # print(C_5.adjacency_list())
# C_5_directly = Graph.new_cycle(5)
# # print(C_5_directly.adjacency_list())
# # print(C_5.is_regular())
# # print(C_5_also.is_regular())
# # print(C_5.degrees())
# C_5_tensor_prod = C_5_also.tensor_product(C_5_directly)
# # print(C_5_tensor_prod.adjacency_list())
# C_5_cartesian_prod = C_5_also.cartesian_product(C_5_directly)
# # print(C_5_cartesian_prod.adjacency_list())
# C_5_strong_prod = C_5_also.strong_product(C_5_directly)
# # print(C_5_strong_prod.adjacency_list())
# # print(C_5.shortest_path_matrix()) #Will need to look at this
# grid_2_3 = Graph.new_grid(2,3,None)
# # print(grid_2_3.adjacency_list())
# cylinder_2_3 = Graph.new_grid(2,3,"cylindrical")
# # print(cylinder_2_3.adjacency_list())
# toroid_3_3 = Graph.new_grid(3,3,"toroidal")
# # print(toroid_3_3.adjacency_list())

# labeler = LPolynomialLabeler((2,1),"allowed")
# C_5_labeling = Labeling([None]*C_5_also.num_verts())
# # print(C_5_labeling.labels())
# C_5_valid_labeling = labeler.complete_labeling(C_5_also, C_5_labeling, 3, 4)
# print(C_5_valid_labeling.labels())
# grid_2_3_valid_labeling = labeler.complete_labeling(grid_2_3, None, 4, 9)
# print(grid_2_3_valid_labeling.labels())
# cylinder_2_3_valid_labeling = labeler.complete_labeling(cylinder_2_3, None, 4, 9)
# print(cylinder_2_3_valid_labeling.labels())
# toroid_3_3_valid_labeling = labeler.complete_labeling(toroid_3_3, None, 5, 16)
# print(toroid_3_3_valid_labeling.labels())

# C_5_labeling.set_label(1,1)
# print(C_5_labeling.labels())
# print(labeler.complete_labeling(C_5_also, C_5_labeling, 3, 4).labels())
# print(labeler.complete_labeling(Graph.new_cycle(13), None, 3, 4).labels())
# print(labeler.complete_labeling(Graph.new_grid(5, 5, 'toroidal'), None, 5, 16).labels())
