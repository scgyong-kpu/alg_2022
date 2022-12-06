# prim 과제했을 때 사용한 edge list 준비
# 파일 이름은 tm_03_학번.py
n_vertices = 12
edges = [
    (0, 6, 194), (0, 7, 59), (0, 9, 372), (1, 11, 125), (2, 4, 345), 
    (2, 8, 246), (2, 9, 293), (2, 10, 166), (4, 8, 82), (4, 10, 164), 
    (5, 6, 119), (5, 7, 232), (6, 7, 169), (8, 9, 286), (8, 10, 193), 
    (9, 10, 150), (3, 4, 100), (3, 8, 200), (1, 5, 150), (5, 11, 250),
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
edges.sort(key=lambda e: e[2]) # edge list 를 가중치로 정렬한다
mst = []
for u, v, w in edges:
  if find_root(u) == find_root(v): continue
  union(u, v)
  mst.append([u,v,w])
  if len(mst) >= n_vertices - 1: break

print(mst)
# [[0, 7, 59], [4, 8, 82], [3, 4, 100], [5, 6, 119], [1, 11, 125], 
#  [9, 10, 150], [1, 5, 150], [4, 10, 164], [2, 10, 166], [6, 7, 169], 
#  [0, 9, 372]]

# 2. Sequence 구하기
adjs = [ [] for _ in range(n_vertices) ]
for u,v,w in mst:
  adjs[u].append(v)
  adjs[v].append(u)
print(adjs)
# [[7, 9], [11, 5], [10], [4], [8, 3, 10], 
#  [6, 1], [5, 7], [0, 6], [4], [10, 0], 
#  [9, 4, 2], [1]]

current = start_index = 3
seq = [ start_index ]
while adjs[current]:
  for i in range(len(adjs[current])):# 
    v = adjs[current][i]
    if not v in seq:
      at = i
      break
  else:
    at = 0
    v = adjs[current][0]

  adjs[current].pop(at)
  seq.append(v)
  current = v
print(seq)
# [3, 4, 8, 4, 10, 9, 0, 7, 6, 5, 1, 11, 1, 5, 6, 7, 0, 9, 10, 2, 10, 4, 3]

# 3. 중복 제거하기
idx = 0
visited = set()
while idx < len(seq):
  v = seq[idx]
  if v in visited:
    seq.pop(idx)
  else:
    idx += 1
    visited.add(v)
seq.append(start_index)
print(seq)
# [3, 4, 8, 10, 9, 0, 7, 6, 5, 1, 11, 2, 3]
