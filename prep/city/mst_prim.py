# MST - Prim Algorithm
from city import five_letter_cities
from edge import edges
import two_d_visualizer as vis
import random
from math import sqrt
from heapdict import heapdict
#pip install heapdict
from collections import defaultdict

class Prim: 
  def __init__(self, cities, edges):
    self.cities = cities
    self.edges = edges
    self.n_cities = len(self.cities)
    self.graph = defaultdict(dict)
    for u,v,w in edges:
      self.graph[u][v] = w
      self.graph[v][u] = w
    self.weights = heapdict()
    self.connects = dict()
    self.total_weight = 0
    self.completed = set()
    self.mst = []

  def start(self, start_index=None):
    if start_index == None:
      start_index = random.randrange(self.n_cities)
    self.start_index = start_index
    print('start at:', self.start_index, self.cities[start_index].name)
    self.weights[start_index] = 0
    self.connects[start_index] = start_index

    while self.weights:
      v, w = self.weights.popitem()
      u = self.connects[v]

      self.mst.append((u, v))
      self.completed.add(v)
      self.total_weight += w

      adjacents = self.graph[v]
      # print(v, adjacents)
      vis.graph_show_adjacents(u, v, w)
      for adj, weight in adjacents.items():
        if adj in self.completed: continue
        if adj in self.weights and weight >= self.weights[adj]: continue
        self.weights[adj] = weight
        self.connects[adj] = v
        vis.graph_update_weight(adj, weight)

      vis.graph_complete()

def make_half_subset():
  min_x, max_x = float('inf'), float('-inf')
  min_y, max_y = float('inf'), float('-inf')
  for c in cities:
    if min_x > c.x: min_x = c.x
    if min_y > c.y: min_y = c.y
    if max_x < c.x: max_x = c.x
    if max_y < c.y: max_y = c.y

  mx = (min_x + max_x) * 3 / 8
  my = (min_y + max_y) * 3 / 8
  city_subset = []
  for c in cities:
    if c.x < mx and c.y < my: city_subset.append(c)

  import mkedge
  edge_subset = mkedge.make_edges(city_subset, 2/3)
  # n_cities = len(city_subset)
  # edge_subset = []
  # for u,v,w in edges:
  #   if u < n_cities and v < n_cities: edge_subset.append((u,v,w))

  print('cities=', len(city_subset), 'edges=', len(edge_subset))
  return city_subset, edge_subset


if __name__ == '__main__':
  random.seed('hello')
  global cities, edges
  cities = five_letter_cities[:100]
  cities, edges = make_half_subset()
  # print(cities)
  vis.init('MST - Prim Algorithm')
  vis.speed = 20

  prim = Prim(cities, edges)
  vis.prim_init(prim)
  prim.start()
  vis.end()
