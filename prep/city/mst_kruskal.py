# MST - Kruskal Algorithm

from city import five_letter_cities
from edge import edges
import two_d_visualizer as vis
from math import sqrt

roots = []
def union(u, v):
  global roots
  uroot = find_root(u)
  vroot = find_root(v)
  roots[vroot] = uroot

def find_root(u):
  if u != roots[u]:
    roots[u] = find_root(roots[u]) # 경로압축
  return roots[u]

def main():
  n_cities = len(cities)

  global roots
  roots = [x for x in range(n_cities)]
  # print(roots)

  weight_edges = sorted(edges, key=lambda e: e[2])
  # for u,v,w in weight_edges:
  #   vis.mst_append(u, v, w)
  # return

  MST = []
  total_cost = 0

  while len(MST) < n_cities - 1 and weight_edges:
    u,v,w = weight_edges.pop(0)
    if find_root(u) == find_root(v):
      continue

    if u > v: u,v = v,u

    c1, c2 = cities[u], cities[v]
    total_cost += w

    MST.append((u, v))
    vis.mst_append(u, v, w, roots)
    union(u, v)
    vis.mst_update_roots(u, v, roots)
    # vis.roots(roots)


    # print('%s -> %s +%.1f = %.1f' % (c1.name, c2.name, w, total_cost))

def make_half_subset():
  min_x, max_x = float('inf'), float('-inf')
  min_y, max_y = float('inf'), float('-inf')
  for c in cities:
    if min_x > c.x: min_x = c.x
    if min_y > c.y: min_y = c.y
    if max_x < c.x: max_x = c.x
    if max_y < c.y: max_y = c.y

  mx = (min_x + max_x) /2#* 4 / 7
  my = (min_y + max_y) /2#* 4 / 7
  city_subset = []
  for c in cities:
    if c.x < mx and c.y < my: city_subset.append(c)

  import mkedge
  edge_subset = mkedge.make_edges(city_subset, 2/3)
  # n_cities = len(city_subset)
  # edge_subset = []
  # for u,v,w in edges:
  #   if u < n_cities and v < n_cities: edge_subset.append((u,v,w))

  print('cities=', len(city_subset), 'edges=', len(edge_subset))
  return city_subset, edge_subset


if __name__ == '__main__':
  global cities, edges
  cities = five_letter_cities[:100]
  cities, edges = make_half_subset()
  # print(cities)
  vis.init('MST - Kruskal Algorithm')
  # print(roots)
  if len(cities) <= 25:
    vis.shows_roots = True
  vis.setup(cities, edges)
  vis.speed = 10
  vis.draw_all_edges(True)
  vis.draw_all_cities()
  vis.update_display()
  main()

  vis.end()
