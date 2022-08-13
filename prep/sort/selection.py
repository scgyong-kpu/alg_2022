# Selection (#th number)

import unsorted
import time
import sort_visualizer
import sort_visualizer_dummy
from random import shuffle

def quickSort(list, left, right): # right=inclusive
  if left >= right: return
  vis.quicksort_push(left, right)
  pivot = partition(list, left, right)
  vis.set_pivot(pivot)
  quickSort(list, left, pivot-1)
  vis.quicksort_fixed()
  quickSort(list, pivot+1, right)
  vis.partition_pop()

def partition(list, left, right):
  pi = left
  pivot = list[pi]

  p, q = left, right + 1
  while True:
    while True:
      p += 1
      if p > right or list[p] >= pivot: break
      if p <= right: vis.set_left(p)
    while True:
      q -= 1
      if q < left or list[q] <= pivot: break
      if q >= left: vis.set_right(q)

    if p >= q: break
    # while p < right and list[p] <= pivot:
    #   p += 1
    #   vis.set_left(p)
    #   print('left:', p)
    # while left < q and list[q] >= pivot:
    #   q -= 1
    #   vis.set_right(q)
    #   print('right:', q)

    # print('pq1:', p, q)

    if p < q:
      vis.set_left(p)
      vis.set_right(q)
      vis.swap(list, p, q)
      list[p], list[q] = list[q], list[p]
  
  # print('lpq:', left, p, q)

  if left != q:
    vis.swap(list, left, q)
    list[left], list[q] = list[q], list[left]
  # print(q, list)

  return q

def selection(arr, left, right, k):
  vis.quicksort_push(left, right)
  pivot = partition(arr, left, right)
  vis.set_pivot(pivot)
  sgs = pivot - left 
  if k < sgs:
    value = selection(arr, left, pivot-1, k)
  elif k == sgs:
    value = arr[pivot]
    global found_answer
    found_answer = True
  else: #sgs < k:
    value = selection(arr, pivot+1, right, k-sgs-1)
  if not found_answer:
    vis.partition_pop()
  return value

if __name__ == '__main__':
  global vis
  vis = sort_visualizer

  vis.init('Selection')
  array = unsorted.numbers[:43]
  k = 16
  shuffle(array)
  vis.setup(array)
  vis.quick = True
  vis.selection = True
  vis.speed = 10#200

  started = time.time()
  value = selection(array, 0, len(array) - 1, k - 1)
  elapsed = time.time() - started
  print("{:2}번째 작은 수는 {:2} 이다".format(k, value), 'Elapsed: %.4fs' % elapsed)
  # print(array)
  vis.end()
