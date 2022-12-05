# prim 과제했을 때 사용한 edge list 
# 파일 이름은 tm_01_학번.py
n_vertices = 18
edges = [
  (0, 9, 210), (0, 13, 498), (0, 16, 606), (1, 2, 203), (1, 8, 217), 
  (1, 16, 537), (2, 8, 322), (2, 16, 269), (3, 4, 189), (3, 7, 534), 
  (3, 8, 466), (3, 11, 371), (3, 12, 284), (3, 17, 407), (4, 7, 193), 
  (4, 11, 273), (4, 12, 181), (4, 15, 316), (5, 6, 224), (5, 14, 178), 
  (5, 17, 628), (6, 10, 202), (6, 11, 448), (6, 17, 272), (7, 11, 142), 
  (7, 12, 141), (7, 15, 249), (9, 13, 457), (9, 16, 281), (10, 17, 405), 
  (11, 12, 215), (11, 17, 176), (12, 15, 255), (12, 17, 373), (13, 14, 241), 
  (13, 16, 265)
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
  # if u 와 v 가 연결된 점이면 넘어가자
  # 연결된 것으로 마킹하자
  # mst 에 추가하자
  # 종료조건 추가하자
  pass

print(mst)
# [[7, 12, 141], [7, 11, 142], [11, 17, 176], [5, 14, 178], [4, 12, 181], 
#  [3, 4, 189], [6, 10, 202], [1, 2, 203], [0, 9, 210], [1, 8, 217], 
#  [5, 6, 224], [13, 14, 241], [7, 15, 249], [13, 16, 265], [2, 16, 269], 
#  [6, 17, 272], [9, 16, 281]]

# 2. Sequence 구하기
# 2-1. MST to Adj-Matrix
adjs = [ [] for _ in range(n_vertices) ]
for u,v,w in mst:
  ...
print(adjs)
# [[9], [2, 8], [1, 16], [4], [12, 3], 
#  [14, 6], [10, 5, 17], [12, 11, 15], [1], [0, 16], 
#  [6], [7, 17], [7, 4], [14, 16], [5, 13], 
#  [7], [13, 2, 9], [11, 6]]

# 2-2. Adj-Matrix to sequence
curr = start_index = 1
seq = [ start_index ]
while True: # 중간에 break 할거니까 일단 무한루프
  adjacents = adjs[curr]
  if not adjacents: break # 더이상 갈 점이 없으면 그만하자

  at = 0    # 아직 안 간 점이 없으면 처음 점으로 그냥 가자
  for i in range(len(adjacents)):
    # seq 에 들어 있지 않은 점 (아직 안 간 점) 을 찾아라
    if not adjacents[i] in seq:
      at = i
      break
  curr = adjacents.pop(at)
  seq.append(curr)
  # 가기로 결정된 점은 갔다고 표시하고 갈수있는점 목록에서 제거한다
  # 가기로 한 점이 이제 curr 이다

print(seq)
# [1, 2, 16, 13, 14, 5, 6, 10, 6, 17, 11, 7, 12, 4, 3, 4, 12, 
#  7, 15, 7, 11, 17, 6, 5, 14, 13, 16, 9, 0, 9, 16, 2, 1, 8, 1]

# 3. 중복 제거하기
while ...:
  if ...:
    index += 1
  else:
    ...pop(index)
print(seq)
# [1, 2, 16, 13, 14, 5, 6, 10, 17, 11, 7, 12, 4, 3, 15, 9, 0, 8, 1]

