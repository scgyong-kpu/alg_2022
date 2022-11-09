from collections import defaultdict
from heapdict import heapdict

edges = [ # 708=China, 725=Reran
  (0, 1, 686), (0, 2, 429), (0, 5, 232), (0, 9, 319), (0, 13, 193), 
  (1, 8, 180), (1, 10, 345), (1, 11, 100), (1, 13, 302), (1, 17, 374), 
  (2, 10, 83), (2, 11, 298), (2, 12, 730), (2, 17, 96), (3, 12, 332), 
  (3, 13, 494), (3, 17, 342), (4, 7, 378), (4, 8, 374), (4, 14, 235), 
  (4, 15, 214), (5, 12, 320), (5, 17, 302), (6, 15, 208), (6, 16, 190), 
  (7, 15, 240), (8, 11, 194), (8, 13, 709), (9, 12, 62), (10, 11, 254), 
  (10, 13, 249), (10, 17, 97), (11, 14, 323), (12, 13, 140), (12, 14, 572), 
  (12, 17, 494), (13, 14, 383), (13, 17, 479), (14, 16, 694), (15, 16, 392)
]
n_vertices = 18#max(max(e[0], e[1]) for e in edges) + 1

total_weight = 0
mst = []

g = defaultdict(dict)
# g[0][1] = 686
for u, v, w in edges:
  g[u][v] = w
  g[v][u] = w

start_index = 4

INF = float('inf')
D = heapdict() #[ INF for _ in range(n_vertices)]
origins = dict()
tree_pts = set()
for v in g[start_index]:
  w = g[start_index][v]
  D[v] = w
  origins[v] = start_index
tree_pts.add(start_index)
origins[start_index] = start_index

print(D)

while D: #len(D) > 0:
  vertex, weight = D.popitem()
  origin = origins[vertex]
  tree_pts.add(vertex)
  mst.append( (origin, vertex, weight) )
  total_weight += weight
  # for adj in g[vertex]: # vertex 에서 연결되는 점 adj 에 대해
  #   w = g[vertex][adj]  # 비용 w 로 연결된다
  for adj, w in g[vertex].items():
    if adj in tree_pts: continue # 이미 결과 tree 에 있는 점이면 거르자
    if adj in D and D[adj] < w: continue # 이미 비용이 덜 드는 점이면 거르자
    D[adj] = w
    origins[adj] = vertex

for v in range(n_vertices):
  path = str(v)#[v]
  orig = v
  while True:
    o = origins[orig]
    if o == orig: break
    path = f'{o} - {path}'
    orig = o
  print(path)
  # print path from start_index to v

print(f'{n_vertices=} {mst=} {total_weight=}')
print(f'sorted={sorted(mst, key=lambda e: e[2])}')
# n_vertices=18 mst=[
#   (9, 12, 62), (2, 10, 83), (2, 17, 96), (1, 11, 100), (12, 13, 140), 
#   (1, 8, 180), (6, 16, 190), (0, 13, 193), (6, 15, 208), (4, 15, 214), 
#   (0, 5, 232), (4, 14, 235), (7, 15, 240), (10, 13, 249), (10, 11, 254), 
#   (11, 14, 323), (3, 12, 332)
# ] total_weight=3331
