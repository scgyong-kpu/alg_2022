import random
from ed_visualizer import EditDistanceVisualizer

class EditDistance:
  def __init__(self, s, t):
    self.s, self.t = s, t
    self.len_s, self.len_t = len(s), len(t)
    self.E = [[-1 for _ in range(self.len_t+1)] for _ in range(self.len_s+1)]

  def start(self):
    # self.E[0] = [i for i in range(self.len_t+1)]
    for j in range(self.len_t+1):
      self.E[0][j] = j
      vis.prepare(0, j)
    for i in range(self.len_s+1):
      self.E[i][0] = i
      vis.prepare(i, 0)

    for i in range(1, self.len_s+1): 
      for j in range(1, self.len_t+1): 
        alpha = 0 if self.s[i-1] == self.t[j-1] else 1
        vis.compare(i, j, alpha)
        # print((self.E[i][j-1]+1, self.E[i-1][j]+1, self.E[i-1][j-1]+alpha))
        self.E[i][j] = min(self.E[i][j-1]+1, self.E[i-1][j]+1, self.E[i-1][j-1]+alpha)
        vis.update()

if __name__ == '__main__':
  # random.seed('hello')
  vis = EditDistanceVisualizer('Edit Distance')
  # cmm = ChainedMatrixMult([10, 20, 5, 15, 30])
  # words = 'equipment', 'effluent'
  # words = 'stro', 'sto'
  # words = 'relevant','elephant'
  # words = 'overflow', 'flower'
  # words = 'automation', 'tomato'
  words = 'automation', 'tomatocan'
  ed = EditDistance(*words)
  vis.setup(ed)
  ed.start()
  vis.end()
