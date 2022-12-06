# prim 과제했을 때 사용한 edge list 
# 파일 이름은 tm_02_학번.py
n_vertices = 19
edges = [
  (0, 1, 565), (0, 4, 473), (0, 6, 124), (0, 18, 448), (1, 4, 166), 
  (1, 6, 257), (1, 7, 532), (1, 16, 323), (2, 5, 169), (2, 8, 172), 
  (2, 11, 255), (2, 15, 526), (3, 8, 154), (3, 11, 381), (3, 12, 240), 
  (3, 13, 464), (3, 15, 375), (3, 16, 220), (3, 17, 318), (4, 10, 280), 
  (5, 9, 374), (5, 13, 484), (6, 10, 179), (6, 13, 445), (6, 17, 93), 
  (7, 13, 211), (7, 17, 313), (9, 12, 47), (9, 13, 239), (9, 14, 217), 
  (11, 14, 430), (12, 13, 305), (12, 14, 228), (15, 18, 249), (17, 18, 386)
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
edges.sort(...)
mst = []
for u,v,w in edges:
  # u,v 를 연결했을때 사이클을 만든다면 관심없다
  # u와 v의 root 조정
  # mst 에 추가
  # 종료조건
  ...
print(mst)
# [[9, 12, 47], [6, 17, 93], [0, 6, 124], [3, 8, 154], [1, 4, 166], 
#  [2, 5, 169], [2, 8, 172], [6, 10, 179], [7, 13, 211], [9, 14, 217], 
#  [3, 16, 220], [9, 13, 239], [3, 12, 240], [15, 18, 249], [2, 11, 255], 
#  [1, 6, 257], [7, 17, 313], [3, 15, 375]]

# 2. Sequence 구하기
# 2-1. MST to Adj-List
adjs = [ [] for _ in range(n_vertices) ]
for u,v,w in mst:
  ...
print(adjs)
# [[6], [4, 6], [5, 8, 11], [8, 16, 12, 15], [1], 
#  [2], [17, 0, 10, 1], [13, 17], [3, 2], [12, 14, 13], 
#  [6], [2], [9, 3], [7, 9], [9], 
#  [18, 3], [3], [6, 7], [15]]

# 2-2. Adj-Matrix to sequence
current = start_index = 2
seq = [ start_index ]
while adjs[current]: # 더 이상 갈 점이 없으면 그만하자
  # while len(adjs[current]) > 0: # 윗줄과 동일한 의미이다

  # 주위에 있는 점들 중 한번도 안 간 곳이 있으면 그리로 간다
  # 갔던 점만 있으면 그 중 하나(첫번째) 로 간다 (사실 하나밖에 안 남았을 터..)
  for i in range(len(adjs[current])):
    at = i
    if not adjs[current][i] in seq:
      break

  # 위 for 루프의 결과에 따라 at 에 어디서 뽑다다가 쓸 지가 결정되어 있다
  current = adjs[current].pop(at) # pop() 으로 제거해 주면서 동시에 다음 점으로 결정해 준다
  seq.append(current) # seq 에 추가해야 한다


print(seq)
# [2, 5, 2, 8, 3, 16, 3, 12, 9, 14, 9, 13, 7, 17, 6, 0, 6, 10, 6, 
#  1, 4, 1, 6, 17, 7, 13, 9, 12, 3, 15, 18, 15, 3, 8, 2, 11, 2]

# 3. 중복 제거하기
visited = set()
index = 0
while index < len(seq):
  if seq[index] in visited:
    seq.pop(index)
  else:
    visited.add(seq[index])
    index += 1
print(seq)
# [2, 5, 8, 3, 16, 12, 9, 14, 13, 7, 17, 6, 0, 10, 1, 4, 15, 18, 11, 2]

