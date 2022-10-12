from vis import ClosestPairVisualizer as Visualizer
# from vis import Dummy as Visualizer
from data_city import City, five_letter_cities
from random import randint, seed, shuffle
from math import sqrt

def distance_sq(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return dx ** 2 + dy ** 2

def distance(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return sqrt(dx ** 2 + dy ** 2)

def brute_force(arr, left, right):
  n_cities = len(cities)
  closest = [-1, -1, float('inf')]
  for i1 in range(left, right+1):
    c1 = cities[i1]
    for i2 in range(i1+1, right+1):
      c2 = cities[i2]
      dist = distance(c1, c2)
      vis.compare(i1,i2,dist)
      if dist < closest[2]:
        closest = [i1, i2, dist]
  return closest

def brute_all():
  n_cities = len(cities)
  vis.push()
  s,e,d = brute_force(cities, 0, n_cities - 1)
  # vis.pop()
  return s,e,d

def devide_and_conquer():
  cities.sort(key=lambda c:c.x)
  for i in range(len(cities)):
    cities[i].index = i
  global y_aligned
  y_aligned = sorted(cities, key=lambda c:c.y)

  s,e,d = closest_pair(cities, 0, len(cities) - 1)
  return s,e,d

def closest_pair(arr, left, right):
  size = right - left + 1
  if size <= 1:
    return -1, -1, 0
  if size == 2:
    s,e,d = left, right, distance(arr[left], arr[right])
    vis.set_closest(left, right, s, e, d)
    return s,e,d
  if size == 3:
    vis.set_phase('Brute force between 3 cities')
    s,e,d = brute_force(arr, left, right)
    vis.set_closest(left, right, s, e, d)
    return s,e,d

  mid = size // 2 + left - 1 # 왼쪽 그룹의 맨 오른쪽 점이므로 1을 뺀다
  # mid is in left group

  vis.push(left, right, mid)

  ls, le, ld = closest_pair(arr, left, mid)    # 왼쪽 그룹에서 가장 까가운 것을 구한다
  rs, re, rd = closest_pair(arr, mid+1, right) # 왼쪽 그룹에서 가장 까가운 것을 구한다

  vis.set_closest(left, -1)
  vis.compare(ls,le,ld)
  vis.set_closest(mid+1, -1)
  vis.compare(rs,re,rd)

  s, e, d = (ls, le, ld) if ld <= rd else (rs, re, rd) # 두 그룹의 해 중에서 더 가까운 것을 구한다
  vis.set_closest(left, right, s, e, d)
  vis.pop()
  return s, e, d                               # 그것이 이번의 해이다 (?)


def main():
  # print(cities)
  # s,e,d = brute_all()
  s,e,d = devide_and_conquer()
  # print(s,e,d)
  print(cities[s],cities[e],d)

if __name__ == '__main__':
  seed('Closest')
  vis = Visualizer('Closest Pair')
  while True:
    beg = randint(0, 100)
    end = beg+4 #randint(beg+10, beg+20)
    cities = five_letter_cities[beg:end]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break
