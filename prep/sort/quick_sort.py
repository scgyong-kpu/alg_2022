# Quick Sort

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

if __name__ == '__main__':
  global vis
  vis = sort_visualizer

  vis.init('Quick Sort')
  array = unsorted.numbers[:43]
  # array = [ 4, 1, 2, 3, 6, 5 ]
  # shuffle(array)
  vis.setup(array)
  vis.quick = True
  vis.speed = 200

  started = time.time()
  quickSort(array, 0, len(array) - 1)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  # print(array)
  vis.end()
