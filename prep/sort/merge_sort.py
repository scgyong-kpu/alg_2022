import unsorted
import time
import sort_visualizer
import sort_visualizer_dummy
from random import shuffle

def mergeSort(array, p, q): #q=inclusive
  global level
  if q <= p: return
  mid = (p + q) // 2
  # print('mergeSort:', p, mid, q)
  vis.partition_push(p, mid, q)
  mergeSort(array, p, mid)
  mergeSort(array, mid+1, q)
  merge(array, p, mid+1, q)
  vis.partition_pop()

def merge(array, left, right, end):
  merged = []
  l, r = left, right
  while l < right and r <= end:
    vis.compare(array, l, r)
    if array[l] <= array[r]:
      merged.append(array[l])
      vis.merged(array, left, l, merged)
      l += 1
    else:
      merged.append(array[r])
      vis.merged(array, left, r, merged)
      r += 1
  while l < right:
    merged.append(array[l])
    vis.merged(array, left, l, merged)
    l += 1
  while r <= end:
    merged.append(array[r])
    vis.merged(array, left, r, merged)
    r += 1

  l = left
  for n in merged:
    array[l] = n
    vis.merge(array, l)
    l += 1
  vis.erase_merged()

if __name__ == '__main__':
  global vis
  vis = sort_visualizer
  
  vis.init('Merge Sort')
  array = unsorted.numbers[:43]
  # shuffle(array)
  vis.setup(array)
  vis.speed = 200

  started = time.time()
  mergeSort(array, 0, len(array) - 1)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  # print(array)
  vis.end()
