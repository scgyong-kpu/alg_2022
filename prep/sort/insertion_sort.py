# Insertion Sort

import unsorted
import time
import sort_visualizer as vis
from random import shuffle

def main(list):
  count = len(list)
  for i in range(1, count):
    for j in range(i, 0, -1):
      vis.selection(list, 0, j, i+1)
      vis.compare(list, j-1, j)
      if list[j-1] > list[j]:
        vis.swap(list, j-1, j)
        list[j-1], list[j] = list[j], list[j-1]
      else: # Enhance 1
        break # Enhance 1

if __name__ == '__main__':
  list = unsorted.numbers[:23]

  vis.init('Insertion Sort')
  # shuffle(list)
  vis.setup(list)
  vis.speed = 100

  started = time.time()
  main(list)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  vis.end()
