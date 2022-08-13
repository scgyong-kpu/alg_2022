from visualizer import *

Color.insert = Color.pastel2[0]
Color.replace = Color.pastel2[2]
Color.delete = Color.pastel2[3]
Color.mouse = Color.set1[0]
Color.equal = Color.gray[2]

class EditDistanceVisualizer(Visualizer):
  def __init__(self, window_title):
    super().__init__(window_title)
    self.data = None

  def setup(self, ed):
    self.data = ed
    self.ctx.ij, self.ctx.alpha = (-1, -1), -1
    self.draw()

  def compare(self, i, j, alpha):
    self.ctx.ij, self.ctx.alpha = (i, j), alpha

  def prepare(self, i, j):
    self.ctx.ij = i, j
    # print('prepare:', self.ctx.__dict__)
    self.draw()
    self.wait(100)

  def update(self):
    self.draw()
    self.wait(1000)

  def draw(self):
    self.calc_coords()
    self.clear()
    self.draw_edit()
    self.draw_table()
    self.update_display()

  def calc_coords(self):
    self.table_h = self.config.screen_height - 2 * self.separator_size
    self.table_w = self.table_h
    self.table_y = self.separator_size
    self.table_x = self.config.screen_width - self.separator_size - self.table_w

    self.cell_w = self.table_w // (self.data.len_t + 2)
    self.cell_h = self.table_h // (self.data.len_s + 2)

  def draw_table(self):
    self.draw_axis()
    for i in range(self.data.len_s+1):
      for j in range(self.data.len_t+1):
        self.draw_cell(i, j)

  def draw_axis(self):
    x = self.table_x + self.cell_w // 2
    y = self.table_y + self.cell_h // 2 + 2 * self.cell_h
    for i in range(self.data.len_s):
      self.draw_text(self.data.s[i], [x,y], Color.dark[2], font=self.big_font)
      y += self.cell_h

    x = self.table_x + self.cell_w // 2 + 2 * self.cell_w
    y = self.table_y + self.cell_h // 2
    for j in range(self.data.len_t):
      self.draw_text(self.data.t[j], [x,y], Color.dark[2], font=self.big_font)
      x += self.cell_w

  def draw_cell(self, y, x):
    rect = [ 
      self.table_x + (x+1) * self.cell_w, 
      self.table_y + (y+1) * self.cell_h, 
      self.cell_w, self.cell_h]
    # if (y,x) == self.ctx.ij:
    #   color = Color.mouse
    if (y,x) in self.inserts:
      color = Color.insert
    elif (y,x) in self.deletes:
      color = Color.delete
    elif (y,x) in self.replaces:
      color = Color.replace
    elif (y,x) in self.equals:
      color = Color.equal
    else:
      color = Color.back
    self.draw_box(rect, color, Color.line)
    value = self.data.E[y][x]
    value = str(value) if value >= 0 else ''
    self.draw_text(value, rect_center(rect), Color.text)

    if (y,x) == self.ctx.ij:
      rect = rect_inflate(rect, -8)
      self.draw_box(rect, line_color=Color.mouse, width=3)

  def on_mouse_motion(self):
    if self.data == None: return
    x, y = pg.mouse.get_pos()

    i = (y - self.table_y) // self.cell_h - 1
    j = (x - self.table_x) // self.cell_w - 1
    if (i >= 0 and i <= self.data.len_s and 
        j >= 0 and j <= self.data.len_t):
      v = self.data.E[i][j]
      self.ctx.ij = (i, j) if v >= 0 else (-1,-1)
    else:
      self.ctx.ij = -1,-1
    self.draw()

  def draw_edit(self):
    x = self.separator_size
    y = self.table_y
    i,j = self.ctx.ij
    s, t = self.data.s[:i], self.data.t[:j]
    self.draw_text('%s => %s' % (s, t), [x, y], horz_center=False, font=self.big_font)
    # ➔ ➜ ➝ ➞ - 유니 코드 문자 백과 사전

    self.inserts = []
    self.deletes = []
    self.replaces = []
    self.equals = []

    self.results = []
    self.add_result(i, j)
    # print('results at:', (i, j), self.results)

    y += 2 * self.separator_size
    x1 = x + self.separator_size
    x2 = x1 + self.separator_size
    x3 = x2 + self.separator_size
    w = 4 * self.separator_size
    h = self.config.font_size * 2

    for f, a, b in self.results:
      if f == 'I':
        color = Color.insert
        s1, s2, s3 = 'Insert', '', a
      elif f == 'D':
        color = Color.delete
        s1, s2, s3 = a, '', 'Delete'
      elif f == 'R':
        color = Color.replace
        s1, s2, s3 = a, '=>', b
      else: # f == 'N'
        color = Color.back
        s1, s2, s3 = a, '-', b
      self.draw_box([x, y, w, h], color, Color.line)
      ty = y + h // 2
      self.draw_text(s1, [x1, ty], Color.text)
      self.draw_text(s2, [x2, ty], Color.text)
      self.draw_text(s3, [x3, ty], Color.text)
      y += h

  def add_result(self, x, y):
    if x < 0 or y < 0: return
    if x == 0 and y == 0: return

    S,T,E = self.data.s, self.data.t, self.data.E
    if x > 0 and y > 0 and E[x-1][y-1] < E[x][y]:
      self.add_result(x-1, y-1)
      self.replaces.append((x, y))
      self.results.append(('R', S[x-1], T[y-1])) # R = replace
    elif x > 0 and E[x-1][y] < E[x][y]:
      self.add_result(x-1, y)
      self.deletes.append((x, y))
      self.results.append(('D', S[x-1], '')) # D = delete
    elif y > 0 and E[x][y-1] < E[x][y]:
      self.add_result(x, y-1)
      self.inserts.append((x, y))
      self.results.append(('I', T[y-1], '')) # I = insert
    else:
      # if x > 1 and y > 1:
      self.add_result(x-1, y-1)
      self.equals.append((x, y))
      self.results.append(('N', S[x-1], T[y-1])) # N = nothing to do

def test():
  # vis.setup()
  pass

if __name__ == '__main__':
  vis = EditDistanceVisualizer('Edit Distance Test')
  test()
  vis.end()

