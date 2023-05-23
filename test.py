import unittest

import OSM_utils
import algorithm

class TestAlgorithm(unittest.TestCase):
  def setUp(self):
    self.G = OSM_utils.get_graph("Amherst", "MA", True)
    self.start = [42.401800, -72.531840]
    self.end = [42.375381, -72.520500]
    self.start_nearest = algorithm.nearest_node(self.G, self.start[1], self.start[0])
    self.end_nearest = algorithm.nearest_node(self.G, self.end[1], self.end[0])
    self.path_maximize, self.shortest_length, self.total_elevation_maximize = (algorithm.dijkstra_path(self.G, self.start_nearest, self.end_nearest, 150, True))
    self.path_minimize, _ , self.total_elevation_minimize= (algorithm.dijkstra_path(self.G, self.start_nearest, self.end_nearest, 150, False))
    self.path_length_maximize = algorithm.path_length(self.path_maximize)
    self.path_length_minimize = algorithm.path_length(self.path_minimize)
    
  def test_graph_generation(self):
    self.assertEqual(len(self.G.nodes), 7275, "Incorrect number of nodes in graph")

  def test_path_length(self):
    
    self.assertTrue(self.path_length_maximize <= self.shortest_length * 1.5, "Path length is larger than allowed") 
    self.assertTrue(self.path_length_minimize <= self.shortest_length * 1.5, "Path length is larger than allowed")       
  def test_elevation(self):
    self.assertTrue(self.total_elevation_maximize >= self.total_elevation_minimize, "Incorrect, maximize elevation should be greater than or euqal to minimize elevaiton")
    self.assertEqual(self.total_elevation_maximize, 87, "Incorrect max elevation")
    self.assertEqual(self.total_elevation_minimize, 78, "Incorrect min elevation")
    
 
 
