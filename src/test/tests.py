"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3

Run test with 'python -m unittest' from test dir
"""

# TODO: tests for graph products. And really, just better tests in general

from graphlib.graph import *
from graphlib.graphmath import *
from graphlib.labeler import *
from graphlib.labeling import *
import unittest

class TestGraphC5(unittest.TestCase):
    """
    Tests for graph model using cycles
    """

    def setUp(self):
        self.adj_list = [
            {1,4},
            {0,2},
            {1,3},
            {2,4},
            {0,3},
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
        self.assertEqual(self.adj_list, self.graph.adjacency_list)

    def test_adjacency_matrix(self):
        self.assertEqual(self.graph.as_adjacency_matrix(), self.adj_mat)

    def test_add_vertex(self):
        self.adj_list.append([])
        self.graph.add_vertex()
        self.assertEqual(self.graph.adjacency_list, self.adj_list)

    def test_add_edge(self):
        self.graph.add_edge(1,3)
        self.adj_list[1].add(3)
        self.adj_list[3].add(1)
        self.assertEqual(self.graph.adjacency_list, self.adj_list)

    def test_new_cycle(self):
        self.assertEqual(self.graph.adjacency_list.sort(), Graph.new_cycle(5).adjacency_list.sort())

    def test_is_regular(self):
        self.assertTrue(self.graph.is_regular())
        self.graph.add_edge(1,3)
        self.assertFalse(self.graph.is_regular())

    def test_remove_vertex(self):
        self.graph.remove_vertex(2)
        self.adj_list = [
            {1,3},
            {0},
            {3},
            {0,2},
        ]
        self.assertEqual(self.graph.adjacency_list, self.adj_list)

    def test_num_verts(self):
        self.assertEqual(self.graph.num_verts(), 5)

    def test_degrees(self):
        self.assertEqual(self.graph.degrees(), [2] * 5)

    def test_new_from_adjacency_matrix(self):
        self.assertEqual(Graph.new_from_adjacency_matrix(self.adj_mat).adjacency_list, self.adj_list)

    def test_shortest_path_matrix(self):
        self.assertEqual(self.graph.shortest_path_matrix(), self.spm)

class TestLPolynomialLabeler(unittest.TestCase):
    """
    Tests for LPolynomialLabeler
    """
    pass #TODO: write these