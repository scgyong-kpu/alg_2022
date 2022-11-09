from data_city import City, five_letter_cities, make_edges
from vis import DijkstraVisualizer as Visualizer
from random import randint, seed, shuffle
from heapdict import heapdict
# heapdict module 을 설치해야 한다. pip install heapdict 로 설치한다.

data_sets = [
  {
    'beg': 340, 'end': 348,
    'edges':[
      (0, 1, 668), (0, 2, 312), (0, 4, 128), (1, 2, 652), (1, 3, 1206), 
      (1, 5, 958), (2, 4, 902), (2, 6, 476), (2, 7, 175), (3, 5, 540), 
      (3, 6, 449), (3, 7, 601), (4, 6, 430), (6, 7, 925)
    ]
  }, {
    'beg': 154, 'end': 165,
    'edges':[
      (0, 2, 524), (0, 4, 133), (0, 7, 422), (0, 9, 786), (1, 2, 127), 
      (1, 8, 139), (2, 5, 491), (2, 8, 248), (3, 6, 460), (3, 7, 431), 
      (3, 9, 715), (3, 10, 528), (4, 5, 440), (4, 7, 325), (4, 9, 709), 
      (5, 7, 250), (5, 8, 329), (5, 9, 204), (5, 10, 497), (6, 7, 682), 
      (6, 10, 114), (7, 9, 377), (7, 10, 345), (9, 10, 298)
    ]
  }, {
    'beg': 146, 'end': 172,
    'edges':[
      (0, 3, 243), (0, 11, 265), (0, 14, 243), (0, 24, 226), (1, 6, 272), 
      (1, 16, 530), (1, 21, 401), (2, 6, 426), (2, 8, 180), (2, 17, 394), 
      (2, 21, 98), (3, 11, 469), (3, 14, 120), (3, 18, 243), (3, 24, 183), 
      (4, 10, 325), (4, 16, 217), (4, 25, 232), (5, 19, 121), (6, 8, 321), 
      (6, 10, 441), (6, 12, 319), (6, 13, 277), (6, 21, 169), (6, 22, 171),
      (7, 9, 222), (7, 10, 231), (8, 12, 58), (8, 13, 416), (8, 21, 329), 
      (8, 22, 204), (9, 10, 201), (9, 16, 177), (9, 23, 288), (10, 13, 495), 
      (0, 16, 305), (11, 14, 475), (11, 20, 247), (11, 24, 73), (13, 15, 506), 
      (13, 21, 167), (14, 17, 276), (14, 24, 260), (14, 25, 232), (15, 17, 446), 
      (15, 19, 466), (15, 21, 223), (16, 23, 425), (17, 18, 260), (18, 25, 241), 
      (19, 20, 196), (20, 24, 482), (21, 22, 240), (22, 23, 232), (23, 25, 220)
    ]
  },
]

n_data_sets = len(data_sets)

# adjacency matric - array of array
def build_graph():
  global graph
  graph = {u: dict() for u in range(n_cities)}
  for u,v,w in edges:
    graph[u][v] = w
    graph[v][u] = w
  print(graph)
  print_adj_matrix()

def print_adj_matrix():
  for u in range(n_cities):
    for v in range(n_cities):
      w = graph[u][v] if v in graph[u] else 0
      print(f'{w:5d}', end='')
    print()
  print()


def main():
  global n_cities
  n_cities = len(cities)

  build_graph()
  print(f'{n_cities} cities, start={cities[start_city_index]}')

  global completed
  completed = set()
  completed.add(start_city_index)

  global weights
  weights = heapdict()
  weights[start_city_index] = 0, start_city_index # weight, from
  vis.append(0, start_city_index)

  global mst
  mst = []
  while weights:
    # print('<', weights)
    v, (w, u) = weights.popitem()
    if u != v:                       # 최초 시작점은 u 와 v 가 같으므로 생략한다
      mst.append((u, v))             # 결과물에 추가한다
    completed.add(v)     # 이번에 v 를 확정한다
    vis.fix(v, u)
    # print('>', weights)
    # print(mst)

    adjacents = graph[v] # v 에 연결되는 점들 중에서
    for adj in adjacents:
      if adj in completed: continue # 이미 완성된 점은 건드리지 말자
      weight = adjacents[adj]
      if adj in weights:    # adj 에 대해 가중치가 저장되어 있다면
        w = weights[adj][0] # 가중치를 가져온다
        if weight < w:      # 가져온 것보다 비용이 적다면
          weights[adj] = weight, v    # 교체한다
          vis.update(weight, adj, v)
        else:
          vis.compare(adj, v, weight)
      else:                        # 저장되어 있지 않다면
        weights[adj] = weight, v   # 추가한다
        vis.append(weight, adj, v)

    # if len(completed) >= 3: break

  vis.finish()
  print(mst)

if __name__ == '__main__':
  vis = Visualizer('Minimum Spanning Tree - Prim')
  idx = 0
  ds = data_sets[idx]
  beg, end = ds['beg'], ds['end']
  cities = five_letter_cities[beg:end]
  City.apply_index(cities)
  edges = ds['edges']
  start_city_index = 0
  while True:
    n_cities = len(cities)
    vis.setup(vis.get_main_module())
    vis.draw()
    main()
    again = vis.end()
    if not again: break
    if vis.restart_lshift:
      idx = (idx + 1) % n_data_sets
      ds = data_sets[idx]
      beg, end = ds['beg'], ds['end']
      cities = five_letter_cities[beg:end]
      City.apply_index(cities)
      edges = ds['edges']
    elif vis.restart_rshift:
      beg = randint(0, 800)
      end = randint(beg+10, beg+100)
      cities = five_letter_cities[beg:end]
      City.apply_index(cities)
      edges = make_edges(cities, 3/5)
    start_city_index = randint(0, n_cities - 1)

