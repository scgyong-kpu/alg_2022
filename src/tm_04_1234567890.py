# prim 과제했을 때 사용한 edge list 
# 파일 이름은 tm_04_학번.py
n_vertices = 18
edges = [
  (0, 1, 686), (0, 2, 429), (0, 5, 232), (0, 9, 319), (0, 13, 193), 
  (1, 8, 180), (1, 10, 345), (1, 11, 100), (1, 13, 302), (1, 17, 374), 
  (2, 10, 83), (2, 11, 298), (2, 12, 730), (2, 17, 96), (3, 12, 332), 
  (3, 13, 494), (3, 17, 342), (4, 7, 378), (4, 8, 374), (4, 14, 235), 
  (4, 15, 214), (5, 12, 320), (5, 17, 302), (6, 15, 208), (6, 16, 190), 
  (7, 15, 240), (8, 11, 194), (8, 13, 709), (9, 12, 62), (10, 11, 254), 
  (10, 13, 249), (10, 17, 97), (11, 14, 323), (12, 13, 140), (12, 14, 572), 
  (12, 17, 494), (13, 14, 383), (13, 17, 479), (14, 16, 694), (15, 16, 392)
]

# 0. union-find 구현
roots = [ x for x in range(n_vertices) ]
def union(u, v):
  global roots
  uroot = find_root(u)
  vroot = find_root(v)
  if uroot > vroot:
    uroot,vroot = vroot,uroot
  roots[vroot] = uroot
def find_root(u):
  if u != roots[u]:
    roots[u] = find_root(roots[u]) # 경로압축
  return roots[u]

# 1. Kruskal Algorithm 으로 MST 구하기
sortedEdges = sorted(edges, ...)
mst = []
while len(mst) < n_vertices - 1:
  u,v,w = edge = sortedEdges.pop(0)
  if ...: continue
  ...
  mst.append(edge)
  # mst.append([u,v,w])

print(mst)
# [[9, 12, 62], [2, 10, 83], [2, 17, 96], [1, 11, 100], [12, 13, 140],
#  [1, 8, 180], [6, 16, 190], [0, 13, 193], [6, 15, 208], [4, 15, 214], 
#  [0, 5, 232], [4, 14, 235], [7, 15, 240], [10, 13, 249], [10, 11, 254], 
#  [11, 14, 323], [3, 12, 332]]


# 2. Sequence 구하기
# 2-1. MST to Adj-List
adjs = [ [] for _ in range(n_vertices) ]
for u,v,w in mst:
  adjs[u].append(v)
  adjs[v].append(u)
print(adjs)
# [[13, 5], [11, 8], [10, 17], [12], [], 
#  [0], [16, 15], [15], [1], [12], 
#  [2, 13, 11], [1, 10, 14], [9, 13, 3], [12, 0, 10], [4, 11], 
#  [4, 7], [], [2]]

# seq = [4,15,6,16,6,...,4]

# 2-2. Adj-Matrix to sequence
current = start_index = 4
seq = [ start_index ]
while adjs[current]: # 더이상 갈 점이 없으면 그만하자
  # while len(adjs[current]) > 0: # 윗줄과 동일한 의미이다

  # 주위에 있는 점들 중 한번도 안 간 곳이 있으면 그리도 간다
  # 갔던 점만 있으면 그 중 하나(첫번째) 로 간다 (사실 하나밖에 안남은 상황이다)

  if False:
    pass
    # for v in adjs[current]:
    #   if not v in seq:
    #     adjs[current].remove(v)
    #     current = v
    #     break
    # else:
    #   current = adjs[current].pop()

    # for i in range(len(adjs[current])):
    #   at = i
    #   if not ... in seq:
    #     break
    # current = adjs[current].pop(at)

  for i in range(len(adjs[current])):
    if not ... in seq:
      current = adjs[current].pop(i)
      break
  else:
    current = adjs[current].pop()

  seq.append(current) # seq 에 current 를 추가한다


print(seq)
# [4, 15, 6, 16, 6, 15, 7, 15, 4, 14, 11, 1, 8, 1, 11, 10, 2, 17,
#  2, 10, 13, 12, 9, 12, 3, 12, 13, 0, 5, 0, 13, 10, 11, 14, 4]

# 3. 중복 제거하기
index = 0
visited = set()
while index < len(seq):
  if seq[index] in visited:
    seq.pop(index)
  else:
    visited.add(seq[index])
    index += 1
print(seq)
# [4, 15, 6, 16, 7, 14, 11, 1, 8, 10, 2, 17, 13, 12, 9, 3, 0, 5, 4]


