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
    vis.finish_mst()
    self.mg = self.build_graph(self.mst_edges) # MST 결과물로 다시 adj-matrix 를 만든다
    self.tsp()
    vis.finish()

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

  def tsp(self):
    self.make_sequence()
    self.find_shortcut()     # 이제 중복된 점만 삭제하면 된다

  def make_sequence(self):
    self.seq = [ self.start_index ] # 방문할 정점들을 기록
    current = self.start_index
    while True:
      if current == self.start_index and not self.mg[self.start_index]:
        break # 시작위치에 돌아왔을 때 더이상 갈 곳이 없으면 그만한다
      adjs = self.mg[current].keys() # 현재 점의 주변 점들이 남아있는지 확인한다
      visit = None
      for k in adjs:
        if visit == None: visit = k  # 첫번째 점을 우선 선택해 둔다
        if k not in self.seq:        # 아직 방문하지 않은 점이면 선택한다
          visit = k
          break
      self.mg[current].pop(visit)    # 선택한 점은 재방문을 막기 위해 삭제한다
      self.seq.append(visit)         # 방문할 정점들에 추가한다
      vis.add_seq(current, visit)
      current = visit                # 선택한 점으로 진행한다

  def find_shortcut(self):
    vis.start_shortcut()
    visited = set()                  # 이미 방문한 점들의 집합
    index = 0
    while index < len(self.seq):     # 중복된 점이 없을때까지 진행
      current = self.seq[index]
      if current in visited:         # 방문했던 점이라면
        vis.update_shortcut(current)
        self.seq.pop(index)          # 현재 점은 삭제한다
      else:                          # 그렇지 않다면 (방문 안한 점이면)
        vis.update_shortcut(current)
        visited.add(current)         # 방문한 점으로 기록하고
        index += 1                   # 다음 점으로 넘어간다

    self.seq.append(self.start_index)
    vis.update_shortcut(self.start_index)

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
