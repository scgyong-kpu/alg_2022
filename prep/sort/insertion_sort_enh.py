# Insertion Sort

import unsorted
import time
import sort_visualizer as vis
from random import shuffle

def main(list):
  count = len(list)
  for i in range(1, count):
    v = list[i]
    j = i
    vis.insertion_init(list, i)
    while j > 0:
      # vis.selection(list, 0, j, i+1)
      vis.bubble(list, j-1, j, i+1, i+1)
      vis.compare(list, j-1, i)
      if list[j-1] > v:
        vis.insertion_move(list, j-1, j)
        list[j] = list[j-1]
        j -= 1
      else:
        break
    vis.insertion_move(list, i, j, value=v)
    list[j] = v

if __name__ == '__main__':
  list = unsorted.numbers[:39]

  vis.init('Insertion Sort')
  # shuffle(list)
  vis.setup(list)
  # vis.speed = 400

  started = time.time()
  main(list)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  vis.end()
