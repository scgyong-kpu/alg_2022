# from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import MergeSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)
  mergeSort(0, count-1)       # 전체 팀을 정렬한다

  print('after :', array)

def insertionSort(left, right): #right=inclusive
  for i in range(left + 1, right + 1):
    v = array[i]
    vis.mark_end(i, v)
    j = i - 1
    while j >= left and array[j] > v:
      vis.shift(j)
      array[j+1] = array[j]
      j -= 1
    vis.insert(i, j+1)
    array[j+1] = v

def mergeSort(left, right): #right=inclusive
  if right <= left: return    # 정렬할 선수들이 없거나 한병뿐이면 할 필요가 없다
  if right < left + 5:
    insertionSort(left, right)
    return
  mid = (left + right) // 2   # 목록을 절반으로 나눈다
  vis.push(left, mid, right)
  mergeSort(left, mid)        # 왼쪽 팀을 정렬한다
  mergeSort(mid+1, right)     # 오른쪽 팀을 정렬한다
  merge(left, mid+1, right)   # 두 팀을 합병한다
  vis.pop()

def merge(left, right, end): # 왼쪽은 [left~right-1], 오른쪽은 [right~end] 이고 end 는 inclusive 이다
  merged = []                        # 임시 저장할 정렬 결과 목록을 준비한다. 
  vis.start_merge(merged, False, left)
  l, r = left, right                 # 각 팀의 첫번째 선수가 입장한다
  while l < right and r <= end:      # 한 팀이라도 팀원이 소진되면 그만한다
    vis.compare(l, r)
    if array[l] <= array[r]:         # 두 팀에서 출전한 선수끼리 겨룬다
      merged.append(array[l])        # 왼쪽팀 선수가 졌으므로 결과 목록에 추가된다
      vis.add_to_merged(l, True)
      l += 1                         # 왼쪽팀은 다음 선수가 나온다
    else:
      merged.append(array[r])        # 오른쪽팀 선수가 졌으므로 결과 목록에 추가된다
      vis.add_to_merged(r, False)
      r += 1                         # 오른쪽팀은 다음 선수가 나온다

  while l < right:                   # 왼쪽팀에 선수가 남아 있다면
    merged.append(array[l])          # 왼쪽팀 선수들은 모두 목록에 추가된다
    vis.add_to_merged(l, True)
    l += 1
  while r <= end:                    # 오른쪽팀에 선수가 남아 있다면
    merged.append(array[r])          # 오른쪽팀 선수들은 모두 목록에 추가된다
    vis.add_to_merged(r, False)
    r += 1

  vis.end_merge()

  array[left:end+1] = merged # 임시 저장되어 있던 결과 목록에 있는 선수들을
                             # 원래의 배열에 옮겨 담는다

''' 성능 측정
count=100 elapsed=0.000
count=1000 elapsed=0.003
count=2000 elapsed=0.006
count=3000 elapsed=0.009
count=4000 elapsed=0.013
count=5000 elapsed=0.017
count=6000 elapsed=0.020
count=7000 elapsed=0.023
count=8000 elapsed=0.027
count=9000 elapsed=0.030
count=10000 elapsed=0.035
count=15000 elapsed=0.052
count=20000 elapsed=0.069
count=30000 elapsed=0.109
count=40000 elapsed=0.148
count=50000 elapsed=0.187
count=100000 elapsed=0.419
count=200000 elapsed=0.851
count=300000 elapsed=1.375
count=400000 elapsed=1.995
count=500000 elapsed=2.590
count=1000000 elapsed=5.320

array copy 를 slicing 을 이용했을 경우
count=100 elapsed=0.000
count=1000 elapsed=0.003
count=2000 elapsed=0.006
count=3000 elapsed=0.008
count=4000 elapsed=0.012
count=5000 elapsed=0.015
count=6000 elapsed=0.018
count=7000 elapsed=0.021
count=8000 elapsed=0.023
count=9000 elapsed=0.025
count=10000 elapsed=0.027
count=15000 elapsed=0.044
count=20000 elapsed=0.060
count=30000 elapsed=0.090
count=40000 elapsed=0.116
count=50000 elapsed=0.149
count=100000 elapsed=0.325
count=200000 elapsed=0.709
count=300000 elapsed=1.142
count=400000 elapsed=1.582
count=500000 elapsed=2.148
count=1000000 elapsed=4.129

2 개 남았을 때 직접비교한 경우
count=100 elapsed=0.000
count=1000 elapsed=0.002
count=2000 elapsed=0.004
count=3000 elapsed=0.007
count=4000 elapsed=0.008
count=5000 elapsed=0.012
count=6000 elapsed=0.014
count=7000 elapsed=0.019
count=8000 elapsed=0.019
count=9000 elapsed=0.023
count=10000 elapsed=0.025
count=15000 elapsed=0.038
count=20000 elapsed=0.058
count=30000 elapsed=0.076
count=40000 elapsed=0.106
count=50000 elapsed=0.138
count=100000 elapsed=0.299
count=200000 elapsed=0.640
count=300000 elapsed=1.017
count=400000 elapsed=1.454
count=500000 elapsed=1.779
count=1000000 elapsed=3.760

20 개 이내이면 insertion sort 를 진행했을 경우
count=100000 elapsed=0.266
count=200000 elapsed=0.580
count=300000 elapsed=0.956
count=400000 elapsed=1.318
count=500000 elapsed=1.658
count=1000000 elapsed=3.501
'''

if __name__ == '__main__':
  seed('Hello')
  vis = Visualizer('Merge Sort')
  while True:
    count = randint(20, 40)
    array = [ randint(1, 99) for _ in range(count) ]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break
