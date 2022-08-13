from city import five_letter_cities
import random
import math
from functools import cmp_to_key
import two_d_visualizer as vis
import heapq

def main():
  global edges
  edges = make_edges(cities)

def make_edges(cities, max_factor=1/4):
  # print('Edge maker')
  edge_set = set()

  min_x, max_x = float('inf'), float('-inf')
  min_y, max_y = float('inf'), float('-inf')
  for c in cities:
    if min_x > c.x: min_x = c.x
    if min_y > c.y: min_y = c.y
    if max_x < c.x: max_x = c.x
    if max_y < c.y: max_y = c.y
  diff_x = max_x - min_x
  diff_y = max_y - min_y
  max_dist = min(diff_x, diff_y) * max_factor

  n_cities = len(cities)
  for c in range(n_cities):
    city = cities[c]

    n, nn, count = 0, 0, random.randint(2, 4)
    while n < count:
      t = random.randrange(n_cities)
      nn += 1
      if nn > 100: 
        print('Too many tries on', c, city.name)
        break
      if t == c: continue
      c1, c2 = (c, t) if c < t else (t, c)
      dist = distance(city, cities[t])
      # print(dist)
      if dist > max_dist: continue
      edge_set.add((c1, c2))
      n += 1

  edge_list = list(edge_set)
  edge_list.sort(key=cmp_to_key(edge_compare))

  # print(edge_list, len(edge_list))
  edges = []
  for c, t in edge_list:
    dist = distance(cities[c], cities[t])
    int_dist = int(dist * random.uniform(0.5, 1.5))
    edges.append((c, t, int_dist))

  # print(edges, len(edges))
  return edges

def make_setcover_edges(cities, max_factor=1/4, max_count=3):
  # print('Edge maker')
  edge_set = set()

  min_x, max_x = float('inf'), float('-inf')
  min_y, max_y = float('inf'), float('-inf')
  for c in cities:
    if min_x > c.x: min_x = c.x
    if min_y > c.y: min_y = c.y
    if max_x < c.x: max_x = c.x
    if max_y < c.y: max_y = c.y
  diff_x = max_x - min_x
  diff_y = max_y - min_y
  max_dist = min(diff_x, diff_y) * max_factor

  n_cities = len(cities)
  for c in range(n_cities):
    nearest = []
    for t in range(n_cities):
      if c == t: continue
      dist = distance(cities[c], cities[t])
      if dist > max_dist: continue
      heapq.heappush(nearest, (dist, c, t))
    for i in range(max_count):
      if not nearest: break
      dist, c, t = heapq.heappop(nearest)
      edge_set.add((c, t))

  edge_list = list(edge_set)
  edge_list.sort(key=cmp_to_key(edge_compare))

  # print(edge_list, len(edge_list))
  edges = []
  for c, t in edge_list:
    dist = distance(cities[c], cities[t])
    int_dist = int(dist * random.uniform(0.8, 1.2))
    edges.append((c, t, int_dist))

  # print(edges, len(edges))
  return edges


def edge_compare(a, b):
  if a[0] == b[0]: return a[1] - b[1]
  return a[0] - b[0]

def distance(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return math.sqrt(dx ** 2 + dy ** 2)

if __name__ == '__main__':
  global cities
  cities = five_letter_cities[:100]
  vis.init('')
  vis.setup(cities)
  random.seed('TUKorea Game 2022-2')
  main()

  for c,t,dist in edges:
    vis.draw_edge(cities[c], cities[t], dist)
    print('  ' + str((c, t, dist)) + ',')

  vis.draw_all_cities()

  vis.update_display()
  vis.end()
