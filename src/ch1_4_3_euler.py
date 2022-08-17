
def start():
  cv = start_vertex # cv: current vertex

  if True: # 나중에 if 를 while 로 변경할 예정이다. 임시로 한 번만 돌기 위해 if 를 썼다
    adjs = len(adj_list[cv]) 
    # 현재 점에서 연결된 점이 몇 개인가?
    # 한개뿐이라면 그리로 가면 되고 여러개라면 선택해야 한다
    if adjs == 1:
      nv = adj_list[cv][0] # 다음 점은 하나밖에 없는 그곳으로 결정하자
      # nv = next vertex
    else:
      # 여러 개 중에서 후보를 고를 예정이다
      # 이번 간선을 삭제하고도 돌아올 수 있다면 가도 좋은 것으로 판단하자
      for cand in adj_list[cv]:
        # cand = 이번 점 으로 가도 좋은지 판단해 보는 후보선수

        # 간선을 임시로 제거해 본다. 
        # 간선을 양방향으로 저장하고 있으므로 둘 다 삭제해야 한다
        adj_list[cv].remove(cand)
        adj_list[cand].remove(cv)

        # cv 에서 cand 까지 연결 되는지 확인한다
        # cv 로부터 연결 가능한 모든 점을 받아서 그 안에 있는지 확인한다
        pts = connected_points(cv)
        is_connected = cand in pts

        # 연결되는지만 확인하려고 간선을 제거한 것이므로
        # 다시 복원시킨다
        adj_list[cv].append(cand)
        adj_list[cand].append(cv)

        # 연결된다면 이번 점으로 진행하기로 한다.
        if is_connected:
          nv = cand      # nv = next vertex
          break

        # 아니라면 다음 후보로 넘어간다


def connected_points(v):
  # 아직 구현 전이므로 임시로 False 를 리턴하는 함수만 만들어 둔다
  return False

def list_all_edges():
  vertex_count = len(adj_list)
  print(f'{vertex_count=}')
  for u in range(vertex_count):
    ends = adj_list[u]
    # print(f'{u=} : {ends=}')
    for v in ends:
      print(f'{u=}, {v=}')

if __name__ == '__main__':
    adj_list = [
      [1, 9], [0, 2], [1, 3, 10, 11], [2, 12], [5, 11], [4, 6], [5, 11], 
      [8, 12], [7, 9, 10, 11], [8, 0], [2, 8], [2, 8, 4, 6], [3, 7]
    ]
    # 인접점 표기 방식으로 그래프를 표현한다
    # adj_list[a] 가 list 이고 그 안에 b 가 있으면 a-b 간선이 있는 것으로 본다

    # list_all_edges()
    start_vertex = 0
    start()
