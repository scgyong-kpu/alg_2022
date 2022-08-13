# Closest Pair

from city import five_letter_cities
import two_d_visualizer as vis
from math import sqrt

class Obj: pass

def brute_force():
  vis.closest_init_brute()
  global min
  min = Obj()
  min.c1 = None
  min.dist = float('inf')
  n_cities = len(cities)
  for a in range(n_cities):
    c1 = cities[a]
    for b in range(a + 1, n_cities):
      c2 = cities[b]
      dist = distance(c1, c2)
      vis.closest_add(c1, c2, dist)
      if min.dist > dist:
        min.dist = dist
        min.c1 = a
        min.c2 = b

def brute_force_2(cities, left, right):
  min_dist = float('inf')
  min_c1 = 0
  min_c2 = 1
  # n_cities = len(cities)
  for a in range(left, right + 1):
    c1 = cities[a]
    for b in range(a + 1, right + 1):
      c2 = cities[b]
      dist = distance_2(c1, c2, min_dist)
      vis.draw_edge(c1, c2, dist, linecolor=1)
      if min_dist > dist:
        min_c1 = a
        min_c2 = b
        min_dist = dist
  vis.closest_dnc_brute(min_c1, min_c2, min_dist)

  return min_c1, min_c2, min_dist

def distance(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return sqrt(dx ** 2 + dy ** 2)

def distance_2(c1, c2, md = False):
  dx = c1.x - c2.x
  if dx < 0: dx = -dx
  if md and dx > md: return dx
  dy = c1.y - c2.y
  if dy < 0: dy = -dy
  if md and dy > md: return dy
  return sqrt(dx ** 2 + dy ** 2)

def devide_and_conquer():
  cities.sort(key=lambda c:c.x)
  for i in range(len(cities)):
    cities[i].index = i
  global y_aligned
  y_aligned = sorted(cities, key=lambda c:c.y)

  vis.closest_init_dnc()
  s,e,d = closest_pair(cities, 0, len(cities) - 1)
  global min
  min = Obj()
  min.c1 = s
  min.c2 = e
  min.dist = d

def closest_pair(arr, left, right):
  size = right - left + 1
  if size <= 1:
    return -1, -1, 0
  if size == 2:
    return left, right, distance(arr[left], arr[right])
  if size == 3:
    return brute_force_2(arr, left, right)

  mid = size // 2 + left - 1 # 왼쪽 그룹의 맨 오른쪽 점이므로 1을 뺀다

  vis.closest_push(left, right, mid)

  ls, le, ld = closest_pair(arr, left, mid)
  vis.closest_left(ls, le, ld)
  rs, re, rd = closest_pair(arr, mid+1, right)

  s, e, d = (ls, le, ld) if ld <= rd else (rs, re, rd)
  cx1 = arr[mid].x - d
  cx2 = arr[mid].x + d

  vis.closest_pop(ls, le, ld, rs, re, rd)

  # mid_area = [c for c in arr if c.x >= cx1 and c.x <= cx2]
  # mid_area.sort(y좌표)

  index1 = min(c.index for c in cities if c.x >= cx1 and c.index >= left)
  index2 = max(c.index for c in cities if c.x <= cx2 and c.index <= right)
  # if index1 < left: index1 = left
  # if index2 > right: index2 = right

  # print('d=%.1f, ld=%.1f, rd=%.1f' % (d, ld, rd), 'i1=%d,i2=%d' % (index1, index2))

  strip = [c for c in y_aligned if c.index >= index1 and c.index <= index2 ]  
  # O(n) search

  vis.closest_strip(cx1, cx2, s, e, d)

  # global dist_call

  n_strip = len(strip)
  # print(strip)
  for s1 in range(n_strip):
    c1 = strip[s1]
    for s2 in range(s1 + 1, n_strip):
      c2 = strip[s2]
      dy = c1.y - c2.y
      if dy < 0: dy = -dy
      if dy > d: break
      dx = c1.x - c2.x
      if dx > d: continue
      # dist_call += 1
      dist = sqrt(dx**2+dy**2)
      vis.closest_dnc_brute(c1, c2, dist)
      if d > dist: 
        d = dist
        s, e = c1.index, c2.index

  vis.closest_close(s, e, d)
  return s, e, d

if __name__ == '__main__':
  global cities
  cities = five_letter_cities[:50]
  # print(cities)
  vis.init('Closest Pair')
  vis.setup(cities)
  vis.draw_all_cities()
  vis.update_display()
  # brute_force()
  devide_and_conquer()
  print('Closest:', cities[min.c1], cities[min.c2], min.dist)
  vis.end()



# print(cities)