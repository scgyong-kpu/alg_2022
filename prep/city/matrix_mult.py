from matrix_visualizer import ChainedMatrixVisualizer
import random

class ChainedMatrixMult:
  def __init__(self, sizes=[]):
    if len(sizes) == 0:
      count = random.randint(5, 10)
      for i in range(count):
        sizes.append(random.randint(3, 20))
    self.sizes = sizes
    self.matrix_count = len(sizes) - 1
    self.C = [[ 0 for _ in range(self.matrix_count + 1) ] for _ in range(self.matrix_count + 1) ]
    self.P = [[ 0 for _ in range(self.matrix_count + 1) ] for _ in range(self.matrix_count + 1) ]

  def start(self):
    count = self.matrix_count
    # print('count=', count)
    for sub_mult_count in range(2, count + 1):
      vis.sub(sub_mult_count)
      max_start = count - sub_mult_count + 1
      # print('sub_mult_count=', sub_mult_count, 'max_start=', max_start)
      for start in range(1, max_start + 1):
        end = start + sub_mult_count - 1 # inclusive end
        vis.range(start, end)
        # print(' [%d, %d]' % (start, end))
        self.C[start][end] = float('inf')
        for k in range(start, end):
          # print('  k=', k)
          temp = self.C[start][k] + self.C[k+1][end] + self.sizes[start-1]*self.sizes[k]*self.sizes[end]
          vis.compare(k)
          if self.C[start][end] > temp:
            self.C[start][end] = temp
            self.P[start][end] = k
            vis.update()
            # vis.update(start, end, k)

    print(self.C[1][count], ':', vis.result(1, count))

if __name__ == '__main__':
  # random.seed('hello')
  vis = ChainedMatrixVisualizer('Chained Matrix Multiplication')
  # cmm = ChainedMatrixMult([10, 20, 5, 15, 30])
  cmm = ChainedMatrixMult()
  vis.setup(cmm)
  cmm.start()
  vis.end()
