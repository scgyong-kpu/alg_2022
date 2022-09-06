# from data_unsorted import numbers
from data_unsorted_a_lot import numbers
from random import randint, seed, shuffle
# from vis import InsertionSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time

def main_level_1():
  print('before:', array)
  count = len(array)

  for i in range(1, count):
    vis.mark_end(i)
    for j in range(i, 0, -1):
      vis.compare(j-1, j)
      if array[j-1] > array[j]:
        vis.swap(j-1, j)
        array[j-1], array[j] = array[j], array[j-1]

  print('after :', array)

def main_level_2():
  print('before:', array)
  count = len(array)

  for i in range(1, count):
    vis.mark_end(i)
    for j in range(i, 0, -1):
      vis.compare(j-1, j)
      if array[j-1] > array[j]:
        vis.swap(j-1, j)
        array[j-1], array[j] = array[j], array[j-1]
      else:
        break

  print('after :', array)

def main():
  # print('before:', array)
  count = len(array)

  for i in range(1, count):
    # vis.mark_end(i, True)
    v = array[i]
    j = i
    while j > 0:
      # vis.compare(j-1, j)
      if array[j-1] > v:
        # vis.shift(j-1, j)
        array[j] = array[j-1]
        # vis.draw()
        j -= 1
      else:
        break
    # vis.shift(i, j, True)
    array[j] = v
    # vis.draw()

  # vis.draw()

  # print('after :', array)

if __name__ == '__main__':
  seed('Hello') # 'Hello' 를 seed 로 고정하여 randint 가 항상 같은 결과가 나오게 한다

  counts = [ 
    100, 1000, 2000, 3000, 4000, 5000, 
    6000, 7000, 8000, 9000, 10000, 15000, 
    20000, 30000, 40000, 50000 ]
  for count in counts:
    array = numbers[:count]
    shuffle(array)
    startedOn = time()
    main()
    elapsed = time() - startedOn
    print(f'{count=} {elapsed=:.3f}')
  exit() 

  vis = Visualizer('Selection Sort')

  while True:
    count = randint(10, 30)
    array = numbers[:count]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()

    again = vis.end()
    if not again: break
