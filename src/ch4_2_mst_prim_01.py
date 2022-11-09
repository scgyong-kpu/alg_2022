from collections import defaultdict
from heapdict import heapdict

edges = [ # 214=Cinch, 231=Owlet
  (0, 9, 210), (0, 13, 498), (0, 16, 606), (1, 2, 203), (1, 8, 217), 
  (1, 16, 537), (2, 8, 322), (2, 16, 269), (3, 4, 189), (3, 7, 534), 
  (3, 8, 466), (3, 11, 371), (3, 12, 284), (3, 17, 407), (4, 7, 193), 
  (4, 11, 273), (4, 12, 181), (4, 15, 316), (5, 6, 224), (5, 14, 178), 
  (5, 17, 628), (6, 10, 202), (6, 11, 448), (6, 17, 272), (7, 11, 142), 
  (7, 12, 141), (7, 15, 249), (9, 13, 457), (9, 16, 281), (10, 17, 405), 
  (11, 12, 215), (11, 17, 176), (12, 15, 255), (12, 17, 373), (13, 14, 241), 
  (13, 16, 265)
]
n_vertices = 18 # max(max(e[0], e[1]) for e in edges) + 1

total_weight = 0
mst = []

g = defaultdict(dict)
for u,v,w in edges:
  g[u][v] = w
  g[v][u] = w
print(g)

start_index = 1

INF = float('inf')
D = heapdict() # { v:INF for v in range(n_vertices) }
origins = dict() # [i for i in range(n_vertices)]
fixeds = set()
for v in range(n_vertices):
  if v in g[start_index]:
    D[v] = g[start_index][v]
    origins[v] = start_index
  else:
    D[v] = INF
print(f'{D=}')
fixeds.add(start_index)
origins[start_index] = start_index

while len(mst) < n_vertices - 1:
  vertex, weight = D.popitem()
  origin = origins[vertex]
  mst.append( (origin, vertex, weight) )
  fixeds.add(vertex)
  total_weight += weight

  # for adj in g[vertex]: # vertex 에서 연결되는 점 adj 에 대해
  #   w = g[vertex][adj]    # 비용 w 로 연결된다
  for adj, w in g[vertex].items():
    if adj in fixeds: continue # 이미 결과 tree 에 있는 점이면 거르자
    if D[adj] < w: continue # 이미 비용이 덜 드는 점이면 거르자
    D[adj] = w
    origins[adj] = vertex

for v in range(n_vertices):
  path = f'{v}'
  orig = v
  while True:
    o = origins[orig]
    if o == orig: break
    path = f'{o} - {path}'
    orig = o

  print(path)

print(f'{n_vertices=} {mst=} {total_weight=}')

# n_vertices=18 mst=[
#   (7, 12, 141), (7, 11, 142), (11, 17, 176), (5, 14, 178), (4, 12, 181), 
#   (3, 4, 189), (6, 10, 202), (1, 2, 203), (0, 9, 210), (1, 8, 217), 
#   (5, 6, 224), (13, 14, 241), (7, 15, 249), (13, 16, 265), (2, 16, 269), 
#   (6, 17, 272), (9, 16, 281)
# ] total_weight=3640
