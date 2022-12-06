from vis import VertexCoverVisualizer as Visualizer
from copy import deepcopy
import data_graph
from random import randrange


class VertexCover:
  def __init__(self, cities, edges, usingSetCover=True):
    self.cities = cities
    self.edges = edges
    self.usingSetCover = usingSetCover
    self.main = self.setCoverMain if usingSetCover else self.maxMatchMain
  def build_graph(self):
    n_cities = len(self.cities)
    self.graph = {u: dict() for u in range(n_cities)}
    for u,v,w in self.edges:
      self.graph[u][v] = w
      self.graph[v][u] = w

  def setCoverMain(self):
    n_cities = len(self.cities)
    n_edges = len(self.edges)
    self.u = { i for i in range(n_edges) }
    self.build_graph()
    self.f = [ set() for _ in range(n_cities) ]
    for i in range(n_edges):
      u,v,w = self.edges[i]
      self.f[u].add(i)
      self.f[v].add(i)
    print(self.u, self.f)
    self.U = deepcopy(self.u)
    self.F = deepcopy(self.f)
    # vis.reset()

    self.C = []
    while self.U:
      max_i = self.F.index(max(self.F, key=lambda s: len(s & self.U)))
      vis.fix(max_i)                 # max_i 번째에 가장 원소가 많이 겹친다
      print(f'fixing {max_i}')
      S = self.F[max_i] # F 에서 U 와의 교집합이 가장 큰 부분집합
      self.U -= S       # U 에서 해당 부분집합의 원소를 제거한다
      print(S, self.U, self.F)
      self.F[max_i] = set()
      self.C.append(S)

    vis.draw()

  def maxMatchMain(self):
    n_cities = len(self.cities)
    n_edges = len(self.edges)
    self.build_graph()
    self.adjs = [ set() for _ in range(n_cities) ]
    print(self.adjs)
    for i in range(n_edges):
      u,v,w = self.edges[i]
      self.adjs[u].add(v)
      self.adjs[v].add(u)
    self.vc = set()
    edge_count = 0
    vertices = list(range(n_cities))
    while edge_count < n_edges:
      print(f'{self.adjs=}, {vertices=}')
      vi = randrange(len(vertices))
      u = vertices.pop(vi)
      print(f'{vi=} {u=} {self.adjs[u]=}')
      if not self.adjs[u]: continue
      v = self.adjs[u].pop()
      print(f'{u=} {v=}')
      vis.matching(u,v)
      for n in (u, v):
        self.vc.add(n)
        print(f'{self.vc=}')

        for k in range(n_cities):
          if k in self.adjs[n]:
            print(f'<{n=} {k=} {self.adjs[n]=} {self.adjs[k]=}')
            self.adjs[n].remove(k)
            if n in self.adjs[k]:
              self.adjs[k].remove(n)
            print(f'>{n=} {k=} {self.adjs[n]=} {self.adjs[k]=}')
            edge_count += 1

      print(f'vc={self.vc} {edge_count=} {n_edges=}')


vis = Visualizer('Vertex Cover')
usingSetCover, gen = True, True
while True:
  if gen:
    d = data_graph.get_next_graph()
    gen = False
  vc = VertexCover(d.cities, d.edges, usingSetCover)
  vis.setup(vc)
  vc.main()
  again = vis.end()
  if not again: break
  if vis.restart_lshift:
    gen = True
  else:
    usingSetCover = not usingSetCover
