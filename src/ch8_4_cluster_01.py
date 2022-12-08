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
    n_cities = len(self.cities)
    if not self.centers:
      # 이번에 최초의 점이 추가되는 것이면 랜덤하게 고른다
      next_center = randint(0, n_cities - 1)
    else:
      # 알려진 거리가 가장 먼 것을 고른다
      # min-heap 이라서 최소값을 고르지만, 
      #  거리에 -1 을 곱한 값이라서 최소값이 가장 먼거리다
      next_center, _ = self.dists.popitem()

    # 추가된 센터를 기록한다
    self.dists[next_center] = (0, next_center)
    self.centers.append(next_center)

    for i in range(n_cities):
      # 이미 센터인 점은 할필요없다
      if i in self.centers: continue 
      # 방금 추가된 센터까지의 거리를 구해서
      d = self.distance_between(next_center, i)
      if not i in self.dists or d < -self.dists[i][0]:
        # 더 가까우면 업데이트한다
        self.dists[i] = (-d, next_center)
      vis.compare(i, next_center,
        d if next_center != self.dists[i][0] else 0)

    clusters = [ [] for _ in self.centers ]
    for i in range(n_cities):
      # 정점 i 가 어느 center 와 가까운지 알아내자
      dist, center = self.dists[i]
      # center 가 몇번째 센터인지 알아내자 (center index)
      ci = self.centers.index(center)
      # ci 번째 클러스터에 i 번째 도시를 넣어주자
      clusters[ci].append(self.cities[i])

    # print(clusters)

    max_r = 0
    for cluster in clusters:
      x, y, r = welzl(cluster)
      if max_r < r: max_r = r
      print(f'{len(cluster)} cities: ({round(x)}, {round(y)}) r: {round(r)}')
    print(f'----- [{len(clusters)} clusters] max R = {max_r} -----')

    vis.draw()

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

    # # INF = float('inf')
    # TOO_SMALL = -1000000000
    # for i in range(len(cities)):
    #   self.dists[i] = (TOO_SMALL, i)

    # first_center = randint(0, len(cities) - 1)
    # self.dists[first_center] = (TOO_SMALL-1, first_center)

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
