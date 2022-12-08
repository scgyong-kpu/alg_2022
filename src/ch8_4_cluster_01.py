from data_city import five_letter_cities, City
from vis import ClusterVisualizer as Visualizer
from heapdict import heapdict
from random import seed, randint
from math import sqrt
from welzl import welzl

class Cluster:
  def __init__(self, cities):
    self.cities = cities
    self.reset()

  def addCenter(self):
    next_center, _ = self.dists.popitem()
    self.dists[next_center] = (0, next_center)
    self.centers.append(next_center)

    # vis.draw()

  # i1 번째 도시와 i2 번째 도시 사이의 거리를 구한다
  def distance_between(self, i1, i2):
    if i1 >= len(self.cities) or i2 >= len(self.cities):
      print(f'{i1=} {i2=} {len(self.cities)=}')
    c1, c2 = self.cities[i1], self.cities[i2]
    return sqrt((c1.x-c2.x)**2+(c1.y-c2.y)**2)

  # cities 만 남겨두고 재시작한다. 시작 도시를 랜덤하게 선택하기 때문에 다른 답을 구해 본다
  def reset(self):
    self.dists = heapdict()
    self.centers = []

    INF = float('inf')
    for i in range(len(cities)):
      self.dists[i] = (INF, i)

    first_center = randint(0, len(cities) - 1)
    self.dists[first_center] = (0, first_center)

# Random Seed 를 정해 두어 랜덤이 정해진 순서대로 나오도록 한다
seed('Cluster')
vis = Visualizer('Clustering')
gen = True
while True:
  if gen:
    # 약 200개까지의 도시를 임의로 선택한다
    beg = randint(0, 100)
    end = randint(beg+15, beg+200)
    cities = five_letter_cities[beg:end]
    # x좌표, y좌표 별로 정렬한다
    cities.sort(key=lambda c: c.x*10000+c.y)
    City.apply_index(cities)
    alg = Cluster(cities)
    vis.setup(alg, True)
    gen = False

  # r 을 누를때마다 클러스터가 하나씩 추가된다
  alg.addCenter()
  if not vis.end(): break

  # LeftShift+R 을 하면 도시는 그대로 두고 처음부터 다시
  if vis.restart_rshift:
    alg.reset()

  # RightShift+R 을 하면 도시들을 랜덤하게 다시 생성한다
  if vis.restart_lshift:
    gen = True
