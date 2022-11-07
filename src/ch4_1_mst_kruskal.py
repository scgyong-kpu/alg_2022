from data_city import City, five_letter_cities, make_edges
from vis import KruskalVisualizer as Visualizer
from random import randint, seed, shuffle

data_sets = [
  {
    'beg': 225, 'end': 244, # 225=Coypu, 243=Rerun
    'edges':[
      (0, 1, 565), (0, 4, 473), (0, 6, 124), (0, 18, 448), (1, 4, 166), 
      (1, 6, 257), (1, 7, 532), (1, 16, 323), (2, 5, 169), (2, 8, 172), 
      (2, 11, 255), (2, 15, 526), (3, 8, 154), (3, 11, 381), (3, 12, 240), 
      (3, 13, 464), (3, 15, 375), (3, 16, 220), (3, 17, 318), (4, 10, 280), 
      (5, 9, 374), (5, 13, 484), (6, 10, 179), (6, 13, 445), (6, 17, 93), 
      (7, 13, 211), (7, 17, 313), (9, 12, 47), (9, 13, 239), (9, 14, 217), 
      (11, 14, 430), (12, 13, 305), (12, 14, 228), (15, 18, 249), (17, 18, 386)
    ],
  }, {
    'beg': 708, 'end': 726, # 708=China, 725=Reran
    'edges':[
      (0, 1, 686), (0, 2, 429), (0, 5, 232), (0, 9, 319), (0, 13, 193), 
      (1, 8, 180), (1, 10, 345), (1, 11, 100), (1, 13, 302), (1, 17, 374), 
      (2, 10, 83), (2, 11, 298), (2, 12, 730), (2, 17, 96), (3, 12, 332), 
      (3, 13, 494), (3, 17, 342), (4, 7, 378), (4, 8, 374), (4, 14, 235), 
      (4, 15, 214), (5, 12, 320), (5, 17, 302), (6, 15, 208), (6, 16, 190), 
      (7, 15, 240), (8, 11, 194), (8, 13, 709), (9, 12, 62), (10, 11, 254), 
      (10, 13, 249), (10, 17, 97), (11, 14, 323), (12, 13, 140), (12, 14, 572), 
      (12, 17, 494), (13, 14, 383), (13, 17, 479), (14, 16, 694), (15, 16, 392)
    ],
  }, {
    'beg': 214, 'end': 232, # 214=Cinch, 231=Owlet
    'edges':[
      (0, 9, 210), (0, 13, 498), (0, 16, 606), (1, 2, 203), (1, 8, 217), 
      (1, 16, 537), (2, 8, 322), (2, 16, 269), (3, 4, 189), (3, 7, 534), 
      (3, 8, 466), (3, 11, 371), (3, 12, 284), (3, 17, 407), (4, 7, 193), 
      (4, 11, 273), (4, 12, 181), (4, 15, 316), (5, 6, 224), (5, 14, 178), 
      (5, 17, 628), (6, 10, 202), (6, 11, 448), (6, 17, 272), (7, 11, 142), 
      (7, 12, 141), (7, 15, 249), (9, 13, 457), (9, 16, 281), (10, 17, 405), 
      (11, 12, 215), (11, 17, 176), (12, 15, 255), (12, 17, 373), (13, 14, 241), 
      (13, 16, 265)
    ],
  },
]

n_data_sets = len(data_sets)

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

def main():
  n_cities = len(cities)

  global roots
  roots = [x for x in range(n_cities)]

  edges.sort(key=lambda e: e[2])
  vis.sort_edges()
  copy = edges[:]

  mst = []
  total_cost = 0

  while len(mst) < n_cities - 1 and copy:
    u,v,w = copy.pop(0)
    if find_root(u) == find_root(v):
      vis.ignore(u, v, w)
      continue

    c1, c2 = cities[u], cities[v]
    total_cost += w
    mst.append((u, v))
    union(u, v)
    vis.append(u, v, w)
    
    # if (len(mst) == 6): break
  vis.finish()

if __name__ == '__main__':
  vis = Visualizer('Minimum Spanning Tree - Ksuskal')
  idx = 0
  while True:
    ds = data_sets[idx]
    beg, end = ds['beg'], ds['end']
    cities = five_letter_cities[beg:end]
    City.apply_index(cities)
    edges = ds['edges']
    vis.setup(vis.get_main_module())
    # vis.draw()
    main()
    again = vis.end()
    if not again: break
    idx = (idx + 1) % n_data_sets

