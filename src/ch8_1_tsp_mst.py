from vis import MstTspVisualizer as Visualizer
from random import randint, seed, shuffle
from heapdict import heapdict
import data_graph

class TspMst:
  def __init__(self, cities, edges):
    self.cities = cities
    self.n_cities = len(cities)
    self.edges = edges

  def build_graph(self, edges):
    g = {u: dict() for u in range(self.n_cities)}
    for u,v,w in edges:
      g[u][v] = w
      g[v][u] = w
    return g

  def main(self):
    self.start_index = randint(0, self.n_cities-1)
    vis.set_start(self.start_index)
    self.g = self.build_graph(self.edges)
    self.mst()

  def mst(self):
    self.completed = set()
    self.completed.add(self.start_index)
    self.weights = heapdict()
    self.weights[self.start_index] = 0
    self.origins = dict()
    self.origins[self.start_index] = self.start_index
    vis.append(0, self.start_index)
    self.mst_edges = []
    while self.weights:
      v, w = self.weights.popitem()
      u = self.origins[v]
      if u != v:
        self.mst_edges.append((u, v, w))
        self.completed.add(v)
      vis.fix(v, u)

      for adj, weight in self.g[v].items():
        if adj in self.completed: continue
        vis.compare(adj, v, weight, True)
        if adj in self.weights and self.weights[adj] < weight: continue
        self.weights[adj] = weight
        self.origins[adj] = v
    vis.finish()

vis = Visualizer('TSP using MST')
gen = True
while True:
  if gen:
    d = data_graph.get_next_graph()
    alg = TspMst(d.cities, d.edges)
    gen = False
  vis.setup(alg)
  alg.main()
  again = vis.end()
  if not again: break
  if vis.restart_lshift: gen = True
