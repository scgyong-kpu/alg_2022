# Set Cover - Greedy Algorithm
from city import five_letter_cities
from edge import edges
import two_d_visualizer as vis
import random
from math import sqrt
from heapdict import heapdict
#pip install heapdict
from collections import defaultdict

class SetCover:
  def __init__(self, cities, edges):
    self.cities = cities
    self.edges = edges
    self.n_cities = len(self.cities)
    self.graph = defaultdict(dict)
    for u,v,w in edges:
      self.graph[u][v] = w
      self.graph[v][u] = w
    self.city_set = set(range(self.n_cities))
    self.covers = []
    for i in range(self.n_cities):
      self.covers.append({i} | set(self.graph[i].keys()))
    # print(self.covers)

  def start(self):
    u = self.city_set
    s = self.covers
    cover = []
    while u:
      max_cover_set = s.index(max(s, key=lambda x: len(u & x)))
      # print(max_cover_set)
      u = u - s[max_cover_set]
      cover.append(max_cover_set)
      s[max_cover_set] = { -1 }
      vis.setcover_show(u, cover, max_cover_set)
    # print(cover)

def make_half_subset():
  min_x, max_x = float('inf'), float('-inf')
  min_y, max_y = float('inf'), float('-inf')
  for c in cities:
    if min_x > c.x: min_x = c.x
    if min_y > c.y: min_y = c.y
    if max_x < c.x: max_x = c.x
    if max_y < c.y: max_y = c.y

  mx = (min_x + max_x) * 7 / 11
  my = (min_y + max_y) * 7 / 11
  city_subset = []
  for c in cities:
    if c.x < mx and c.y < my: city_subset.append(c)

  import mkedge
  edge_subset = mkedge.make_setcover_edges(city_subset, 1, 7)

  print('cities=', len(city_subset), 'edges=', len(edge_subset))
  return city_subset, edge_subset


if __name__ == '__main__':
  random.seed('hello')
  global cities, edges
  cities = five_letter_cities[:100]
  cities, edges = make_half_subset()
  # print(cities)
  vis.init('Set Cover - Greedy Algorithm')
  # vis.speed = 2
  setcover = SetCover(cities, edges)
  vis.setcover_init(setcover)
  setcover.start()
  vis.end()
