# Cocktail Shaker

import unsorted
import time
import sort_visualizer as vis
from random import shuffle

def main(list):
  count = len(list)
  start, end = 0, count - 1
  forward = True
  while start < end:
    if forward:
      ls, le, inc = start, end, 1
    else:
      ls, le, inc = end, start, -1
    last = start + inc
    for i in range(ls, le, inc):
      vis.bubble(list, start, i, end+1, count)
      if forward:
        i1, i2 = i, i+1
      else:
        i1, i2 = i-1, i
      vis.compare(list, i1, i2)
      if list[i1] > list[i2]:
        vis.swap(list, i1, i2)
        list[i1], list[i2] = list[i2], list[i1]
        last = i+inc
    if forward:
      end = last - 1
      forward = False
    else:
      start = last + 1
      forward = True
  vis.bubble(list, 0, None, 0, count)

  # print(list) 



if __name__ == '__main__':
  list = unsorted.numbers[:40]

  vis.init('Cocktail Shaker Sort')
  # shuffle(list)
  vis.setup(list)
  vis.speed = 100

  started = time.time()
  main(list)
  elapsed = time.time() - started
  print('Elapsed: %.4fs' % elapsed)
  vis.end()
