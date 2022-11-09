from collections import defaultdict
#pip install heapdict
from heapdict import heapdict

n_vertices = 12
edges = [
    (0, 6, 194), (0, 7, 59), (0, 9, 372), (1, 11, 125), (2, 4, 345), 
    (2, 8, 246), (2, 9, 293), (2, 10, 166), (4, 8, 82), (4, 10, 164), 
    (5, 6, 119), (5, 7, 232), (6, 7, 169), (8, 9, 286), (8, 10, 193), 
    (9, 10, 150), (3, 4, 100), (3, 8, 200), (1, 5, 150), (5, 11, 250),
]

g = defaultdict(dict)
for u,v,w in edges:
    pass # edges 의 내용을 g 로 옮김 (adj-matrix 형태로)
    g[u][v] = w
    g[v][u] = w    
print(g)

D = heapdict() # Key=정점index, Value=가중치
origins = dict() # Key=정점, Value=어느정점에서왔는지
tree_vertices = set() # 완성된결과물에 포함된 정점들

mst = [] # 결과물

start_index = 3
# INF = float('inf')
# for i in range(n_vertices):
#     if i in g[start_index]:
#         D[i] = g[start_index][i]
#     else:
#         D[i] = INF
# # D[start_index] = 0
# print(D)
tree_vertices.add(start_index)
D[start_index] = 0
origins[start_index] = start_index
total_weight = 0
while D: # len(D) > 0:
    k, v = D.popitem()
    orig = origins[k] # 점 k 가 어디에서 왔는지 알아낸다
    if orig != k:
        mst.append( (orig, k, v) )
        tree_vertices.add(k)
        total_weight += v

    for adj, weight in g[k].items(): # k 에서 연결되는 점들에 대해 
                                     # adj 점까지 weight 비용으로 연결된다
        if adj in tree_vertices: continue # 이미 결과 tree 에 있는 점이면 거르자
        if adj in D and D[adj] < weight: continue # 이미 비용이 덜 드는 점이면 거르자
        D[adj] = weight # 비용을 업데이트한다
        origins[adj] = k # adj 까지는 k 를 통해서 오는 것이 가장 비용이 싸다

# print(origins)
for i in range(n_vertices):
    path = str(i)
    orig = i
    while origins[orig] != orig:
        path = f'{origins[orig]}-{path}'
        orig = origins[orig]
    print(path)

print(f'{mst=} {total_weight=}')
mst.sort(key=lambda x:x[2])
print(f'{mst=} {total_weight=}')
# mst = [
#     (0, 7, 59), (4, 8, 82), (3, 4, 100), (5, 6, 119), (1, 11, 125), 
#     (9, 10, 150), (1, 5, 150), (4, 10, 164), (2, 10, 166), (6, 7, 169),
#     (8, 10, 193)
# ]
