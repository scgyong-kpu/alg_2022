# Cocktail Shaker

import unsorted
import time
import sort_visualizer as vis
from random import shuffle

def main(list):
  count = len(list)
  last_parent_index = count // 2 - 1
  for n in range(last_parent_index, -1, -1):
    vis.heap_set_root(n)
    heapify(list, n, count)
  vis.heap_set_root(None)

  last_sort_index = count - 1
  while last_sort_index > 0:
    vis.heap_compare(list, 0, last_sort_index, 0, last_sort_index + 1)
    vis.swap(list, 0, last_sort_index)
    list[0], list[last_sort_index] = list[last_sort_index], list[0]
    heapify(list, 0, last_sort_index)
    last_sort_index -= 1

  # vis.heapsort(list, 0, 0)

def heapify(arr, root, size):
  vis.heapsort(arr, root, size)
  lc = root * 2 + 1
  if lc >= size: return
  child = lc
  rc = root * 2 + 2
  if rc < size:
    vis.heap_compare(arr, rc, lc, root, size)
    if arr[rc] > arr[lc]:
      child = rc

  vis.heap_compare(arr, root, child, root, size)
  if arr[root] < arr[child]:
    vis.swap(list, root, child)
    arr[root], arr[child] = arr[child], arr[root]
    vis.heapsort(arr, root, size)
    heapify(arr, child, size)

if __name__ == '__main__':
  list = unsorted.numbers[:13]

  vis.init('Heap Sort')
  # shuffle(list)
  vis.setup(list)
  # vis.speed = 200

  started = time.time()
  main(list)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  vis.end()
