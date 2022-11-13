from data_city import City, five_letter_cities, make_edges
from vis import CitySetCoverVisualizer as Visualizer
from random import randint, seed, shuffle
from copy import deepcopy

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

def build_graph():
  global graph
  graph = {u: dict() for u in range(n_cities)}
  for u,v,w in edges:
    graph[u][v] = w
    graph[v][u] = w

def main():
  global n_cities
  n_cities = len(cities)

  build_graph()

  global u, f, U, F
  f = [
    set(list(d.keys()) + [u]) for u,d in graph.items()
  ]
  print(f)
  U = deepcopy(u)
  F = deepcopy(f)
  vis.draw()
  vis.wait(1000)

  # global C
  # C = []
  # while U:
  #   max_i = F.index(max(F, key=lambda s: len(s & U)))
  #   vis.fix(max_i)                 # max_i 번째에 가장 원소가 많이 겹친다
  #   S = F[max_i] # F 에서 U 와의 교집합이 가장 큰 부분집합
  #   U -= S       # U 에서 해당 부분집합의 원소를 제거한다
  #   F[max_i] = set()
  #   C.append(S)
  #   print(f'{U=}, {C=}')
  # vis.draw()


if __name__ == '__main__':
  vis = Visualizer('Set Cover - Cities')
  idx = 0
  ds = data_sets[idx]
  beg, end = ds['beg'], ds['end']
  cities = five_letter_cities[beg:end]
  City.apply_index(cities)
  edges = ds['edges']
  start_city_index = 0
  while True:
    n_cities = len(cities)
    u = set(range(0, n_cities))
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
      end = randint(beg+10, beg+40)
      cities = five_letter_cities[beg:end]
      City.apply_index(cities)
      edges = make_edges(cities, 3/5)
    start_city_index = randint(0, n_cities - 1)

