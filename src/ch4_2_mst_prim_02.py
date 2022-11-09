from collections import defaultdict
from heapdict import heapdict # pip install heapdict

edges = [ # 225=Coypu, 243=Rerun
  (0, 1, 565), (0, 4, 473), (0, 6, 124), (0, 18, 448), (1, 4, 166), 
  (1, 6, 257), (1, 7, 532), (1, 16, 323), (2, 5, 169), (2, 8, 172), 
  (2, 11, 255), (2, 15, 526), (3, 8, 154), (3, 11, 381), (3, 12, 240), 
  (3, 13, 464), (3, 15, 375), (3, 16, 220), (3, 17, 318), (4, 10, 280), 
  (5, 9, 374), (5, 13, 484), (6, 10, 179), (6, 13, 445), (6, 17, 93), 
  (7, 13, 211), (7, 17, 313), (9, 12, 47), (9, 13, 239), (9, 14, 217), 
  (11, 14, 430), (12, 13, 305), (12, 14, 228), (15, 18, 249), (17, 18, 386)
]
n_vertices = 19 #max(max(e[0], e[1]) for e in edges) + 1

g = defaultdict(dict)
for u, v, w in edges:
  g[u][v] = w
  g[v][u] = w

start_index = 2

INF = float('inf')
D = heapdict()
origins = dict()
completed = set()

# for i in range(n_vertices):
#   if i in g[start_index]:
#     D[i] = g[start_index][i]
#   # else:
#   #   D[i] = INF
# completed.add(start_index)
origins[start_index] = start_index
D[start_index] = 0

total_weight = 0
mst = []

while D: #len(D) > 0:
  vertex, weight = D.popitem()
  completed.add(vertex)
  origin = origins[vertex]
  if vertex != origin:
    mst.append( (origin, vertex, weight) )
    total_weight += weight

  # for adj in g[vertex]:
  #   w = g[vertex][adj]
  for adj, w in g[vertex].items(): # k 에서 연결되는 점들에 대해 
                                   # adj 점까지 w 비용으로 연결된다
    if adj in completed: continue # 이미 결과 tree 에 있는 점이면 거르자
    if adj in D and D[adj] < w: continue # 이미 비용이 덜 드는 점이면 거르자
    D[adj] = w
    origins[adj] = vertex

for v in range(n_vertices):
  path = str(v)
  orig = v
  while True:
    o = origins[orig]
    if (o == orig): break
    orig = o
    path = f'{orig}-{path}'
  print(path)

mst.sort(key=lambda e:e[2])
print(f'{n_vertices=} {mst=} {total_weight=}')
# n_vertices=19 mst=[
#   (9, 12, 47), (6, 17, 93), (0, 6, 124), (3, 8, 154), (1, 4, 166), 
#   (2, 5, 169), (2, 8, 172), (6, 10, 179), (7, 13, 211), (9, 14, 217), 
#   (3, 16, 220), (9, 13, 239), (3, 12, 240), (15, 18, 249), (2, 11, 255), 
#   (1, 6, 257), (7, 17, 313), (3, 15, 375)
# ] total_weight=3680
