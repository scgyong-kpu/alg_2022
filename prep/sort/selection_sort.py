# Selection Sort

import unsorted
import time
import sort_visualizer as vis
from random import shuffle

def main(list):

  for a in range(len(list)):
    min = list[a]
    at = a
    vis.selection(list, a, at)
    for b in range(a + 1, len(list)):
      vis.compare(list, at, b)
      if min > list[b]:
        min = list[b]
        vis.selection(list, a, b)
        at = b
    vis.swap(list, a, at)
    list[a], list[at] = list[at], list[a]
    vis.selection()

  # print(list) 



if __name__ == '__main__':
  list = unsorted.numbers[:30]

  vis.init('Selection Sort')
  shuffle(list)
  vis.setup(list)
  vis.speed = 200

  started = time.time()
  main(list)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  vis.end()
