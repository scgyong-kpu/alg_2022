from vis import SetCoverVisualizer as Visualizer
from random import randint, seed
from copy import deepcopy

# Set Cover 시작
u={1,2,3,4,5,6,7,8,9,10}
f=[
  {1,2,3,8},
  {1,2,3,4,8},
  {1,2,3,4},
  {2,3,4,5,7,8},
  {4,5,6,7},
  {5,6,7,9,10},
  {4,5,6,7},
  {1,2,4,8},
  {6,9},
  {6,10},
]

def main():
  C = [] # 결과를 저장할 배열

  global U
  while U:
    max_i, max_c = -1, 0
    for i in range(len(F)):        # subset 들을 대상으로 Loop 를 돈다
      cnt = len(U & F[i])          # 겹치는 갯수는 교집합의 원소수와 같다
      vis.comp(i, None, cnt)
      if max_c < cnt:              # 겹치는 갯수 중 max 를 max_c,
        max_i, max_c = i, cnt      # 그 위치를 max_i 에 저장한다 
    vis.fix(max_i)                 # max_i 번째에 가장 원소가 많이 겹친다
    U -= F[max_i]    # U 에서 가장 많이 겹치는 그룹의 원소를 제거한다
    S = F.pop(max_i) # F 에서 해당 subset 집합을 제거하고
    C.append(S)      # 결과 배열인 C 에 넣는다
    print(f'{C=}')

# print(u)              # u 의 원소를 모두 출력
# print(f[1], f[5])     # f[1] 과 f[5] 를 각각 출력
# print(f[1] | f[5])    # f[1] 과 f[5] 의 합집합을 출력해 보면 u 와 같다
# 따라서 위 두 집합을 선택하면 최소 선택으로 u 를 모두 cover 할 수 있다

seed('SetCover')
vis = Visualizer('Set Cover - Simple Set')
while True:
  U = deepcopy(u) # 원본에서 제거하면서 진행할 것이므로
  F = deepcopy(f) # 복사를 해 둔다
  vis.setup(vis.get_main_module())
  vis.reset()
  main()
  vis.draw()
  again = vis.end()
  if not again: break

  n_cities = randint(15, 30)
  print(f'{n_cities=}')
  u = set()
  f = []
  si = 0
  while True:
    s = set()
    sc = randint(2, 12)
    for i in range(sc):
      ci = (si + randint(1, 12)) % n_cities
      s.add(ci)
    u |= s
    f.append(s)
    # print(s)
    if len(u) == n_cities: break

    si = (si + 1) % n_cities

