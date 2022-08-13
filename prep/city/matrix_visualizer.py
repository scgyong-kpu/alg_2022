import pygame as pg
from random import randint

screen_size = [ 800, 600 ]
screen_size = [ 1000, 700 ]
# screen_size = [ 1600, 900 ]
screen_size = [ 2000, 1200 ]
# screen_size = [ 3500, 2200 ]

WAIT_ONE_FRAME_MILLIS = 15
FONT_SIZE = screen_size[0] // 80
SEPARATOR_SIZE = FONT_SIZE * 4

def color_argb(value): 
  value = value.lstrip('#')
  lv = len(value)
  return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def color_argb_array(array): 
  return [ color_argb(value) for value in array ]

class Color:
  pair = color_argb_array(["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"])
  pastel1 = color_argb_array(["#fbb4ae","#b3cde3","#ccebc5","#decbe4","#fed9a6","#ffffcc","#e5d8bd","#fddaec","#f2f2f2"])
  pastel2 = color_argb_array(["#b3e2cd","#fdcdac","#cbd5e8","#f4cae4","#e6f5c9","#fff2ae","#f1e2cc","#cccccc"])
  set1 = color_argb_array(["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33","#a65628","#f781bf","#999999"])
  set2 = color_argb_array(["#66c2a5","#fc8d62","#8da0cb","#e78ac3","#a6d854","#ffd92f","#e5c494","#b3b3b3"])
  set3 = color_argb_array(["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"])
  dark = color_argb_array(["#1b9e77","#d95f02","#7570b3","#e7298a","#66a61e","#e6ab02","#a6761d","#666666"])
  operator = dark[0]
  operand = dark[2]
  line = dark[0]
  back = color_argb('#ffffff')
  text = color_argb('#00001f')
  light_text = dark[7]

class Visualizer:
  def __init__(self, window_title):
    global screen
    pg.init()
    screen = pg.display.set_mode(screen_size)
    # w, h = pg.display.get_surface().get_size()
    # print('w:', w, 'h:', h)
    pg.display.set_caption(window_title)

    global smFont, bigFont
    smFont = pg.font.SysFont("arial", FONT_SIZE) 
    bigFont = pg.font.SysFont("arial", FONT_SIZE * 2)

    self.clear()

    self.speed = 1

  speeds = [ 200, 1, 2, 3, 4, 5, 10, 20, 50, 100 ]

  def clear(self, color = (255,255,255)):
    screen.fill(color)

  def wait(self, millis):
    millis = int(millis / self.speed)
    if millis < WAIT_ONE_FRAME_MILLIS: millis = WAIT_ONE_FRAME_MILLIS

    pg.time.wait(millis)
    self.loop, first = True, True
    while self.loop:
      if first:
        self.loop, first = False, False
      for e in pg.event.get():
        if self.handle_event(e):
          continue
        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
          self.loop = True
        elif e.type == pg.KEYUP and e.key == pg.K_SPACE:
          self.loop = False

  def handle_event(self, e):
    if e.type == pg.QUIT:
      pg.quit()
      self.loop = False
      return True
    elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
      pg.quit()
      self.loop = False
      return True
    elif e.type == pg.KEYDOWN and e.key >= pg.K_0 and e.key <= pg.K_9:
      self.speed = self.speeds[e.key - pg.K_0]
    elif e.type == pg.MOUSEMOTION:
      return self.on_mouse_motion()
    return False

  def on_mouse_motion(self): 
    return True

  def wait_for_keydown(self):
    self.loop = True
    while self.loop:
      for e in pg.event.get():
        if self.handle_event(e):
          continue
        if e.type == pg.KEYDOWN:
          self.loop = False

  def end(self):
    self.loop = True
    while self.loop:
      for e in pg.event.get():
        self.handle_event(e)
    pg.quit()

  def update_display(self):
    pg.display.flip()

  def draw_text(self, text, xy, color=Color.text, horz_center=True, font=None):
    if font == None: font = smFont
    img = font.render(text, True, color)
    if (horz_center):
      rect = img.get_rect(center = xy)
      screen.blit(img, rect)
    else:
      screen.blit(img, xy)

  def draw_box(self, box, body_color, line_color=None, width=1):
    pg.draw.rect(screen, body_color, box)
    if line_color != None:
      pg.draw.rect(screen, line_color, box, width)

class Matrix:
  def __init__(self, rows, cols, rand=0):
    self.rows, self.cols = rows, cols
    self.data = []#[ randint(1, 99) for x in range(cols) ] for y in range(rows) ]
    for r in range(rows):
      self.data.append([])
      for c in range(cols):
        v = randint(1, rand) if rand > 0 else 0
        self.data[r].append(v)
      #   print('%2d' % self.data[r][c], end=' ')
      # print()

class MatrixVisualizer(Visualizer):
  def __init__(self, window_title):
    super().__init__(window_title)

  def setup(self, a, b, c):
    self.a, self.b, self.c = a, b, c
    a.xi = 1
    b.xi = a.xi + a.cols + 2
    c.xi = b.xi + b.cols + 2
    a.ci, b.ci, c.ci = 1, 2, 3
    self.cols = a.cols + b.cols + c.cols + 6
    self.rows = max(a.rows, b.rows, c.rows) + 2
    w = screen_size[0] // self.cols
    h = screen_size[1] // self.rows
    self.cell_w, self.cell_h = w, h

    self.times = 0

  def draw(self):
    self.draw_matrix(self.a)
    self.draw_matrix(self.b)
    self.draw_matrix(self.c)

    x = int((self.b.xi - 1) * self.cell_w)
    y = screen_size[1] // 2
    self.draw_text('x', [x, y], Color.text, font=bigFont)
    x = int((self.c.xi - 1) * self.cell_w)
    self.draw_text('=', [x, y], Color.text, font=bigFont)

    xy = [self.cell_w, screen_size[1] - 2 * FONT_SIZE]
    self.draw_text('mult times = %d' % self.times, xy, horz_center=False)

    self.update_display()

  def coords(self, m):
    x = int(m.xi * self.cell_w)
    y = (self.rows - m.rows) * self.cell_h // 2
    w, h = self.cell_w, self.cell_h
    return x, y, w, h

  def draw_matrix(self, m):
    sx, sy, w, h = self.coords(m)
    mg = w // 5
    box = [ sx - mg, sy - mg, (m.cols) * w + 2 * mg, (m.rows) * h + 2 * mg ]
    self.draw_box(box, Color.pastel1[m.ci], Color.set1[m.ci])

    txy = [sx + m.cols * w // 2, sy - mg - FONT_SIZE]
    self.draw_text('%d x %d' % (m.rows, m.cols), txy, Color.text, font=bigFont)

    sx += w // 2
    y = sy + h // 2
    for row in m.data:
      x = sx
      for v in row:
        self.draw_text(str(v), [x,y], Color.text)
        x += self.cell_w
      y += self.cell_h

  def start(self):
    for r in range(self.c.rows):
      for c in range(self.c.cols):
        for i in range(self.a.cols):
          self.times += 1
          self.clear()
          self.draw()
          self.draw_cell(self.a, r, i)
          self.draw_cell(self.b, i, c)
          self.draw_result_cell(r, c, i)
          self.c.data[r][c] += self.a.data[r][i] * self.b.data[i][c]
          self.update_display()
          self.wait(500)

    self.draw()
    self.wait(500)

  def draw_cell(self, m, r, c, shows_value=True):
    sx, sy, w, h = self.coords(m)
    x = sx + c * w
    y = sy + r * h
    box = [ x, y, w, h ]
    self.draw_box(box, Color.pastel2[m.ci], Color.set2[m.ci])
    if shows_value:
      x += w // 2
      y += h // 2
      self.draw_text(str(m.data[r][c]), [x, y], Color.text)
    return tuple(box)

  def draw_result_cell(self, r, c, i):
    x,y,w,h = self.draw_cell(self.c, r, c, False)
    x += w // 2
    y += (h - 3 * FONT_SIZE) // 2
    prev_value = self.c.data[r][c]
    mult_value = self.a.data[r][i] * self.b.data[i][c]
    sum_value = prev_value + mult_value
    line_gap = FONT_SIZE * 3 // 4
    self.draw_text(str(prev_value), [x, y], Color.operand)
    y += line_gap
    self.draw_text('+', [x, y], Color.operator)
    y += line_gap
    self.draw_text(str(mult_value), [x, y], Color.operand)
    y += line_gap
    self.draw_text('=', [x, y], Color.operator)
    y += line_gap
    self.draw_text(str(sum_value), [x, y], Color.text)

class ChainedMatrixVisualizer(Visualizer):
  def __init__(self, window_title):
    super().__init__(window_title)
    self.sub_mult_count = self.i_start = self.i_end = self.i_k = -1

  def setup(self, cmm):
    self.data = cmm
    self.max = max(cmm.sizes)
    div = max(5, cmm.matrix_count - 1)
    self.header_height = screen_size[1] // div
    self.header_cell_width = screen_size[0] // cmm.matrix_count
    self.msize = min(self.header_height * 4 // 5, self.header_cell_width)
    print(*self.cell_rect(2,1))
    self.draw()

  def sub(self, sub_mult_count):
    self.sub_mult_count = sub_mult_count

  def range(self, start, end):
    self.i_start, self.i_end = start, end
    self.i_k = -1

  def compare(self, k):
    self.i_k = k
    self.update(False)

  def update(self, emp=True):
    self.emp = emp
    self.draw()
    self.wait(1000)
    
  def draw(self):
    self.clear()
    count = self.data.matrix_count
    for i in range(count):
      self.draw_mini_matrix(i)
      if i > 0:
        self.draw_adj_mult(i)

    for start in range(1, count + 1):
      for end in range(start + 1, count + 1):
        self.draw_c(start, end)
      #   print(self.data.C[y][x], end=' ')
      # print()

    if self.i_start >= 0:
      self.mark_header(self.i_start, self.i_end, self.i_k)

    self.draw_axis()

    self.update_display()

  def result(self, i, j):
    P = self.data.P
    if i == j:
      return 'A' + str(i)
    if P[i][j] == 0:
      return ''
    # print('result():', i, j, P[i][j])
    return '(' + self.result(i, P[i][j]) + '×' + self.result(P[i][j]+1, j) + ')'

  def mark_header(self, start, end, k=-1):
    x = self.header_cell_width * (start - 1)
    w = self.header_cell_width * (end - start + 1)
    rect = [x, 2, w, self.header_height - 4]
    pg.draw.rect(screen, Color.line, rect, 1)

    if k >= 0:
      mx = self.header_cell_width * k
      my = self.header_height // 2
      self.draw_text('×', [mx, my], Color.text, font=bigFont)
      # w1 = self.header_cell_width * (k - start + 1)
      # r1 = [ x + 4, 4, w1 - 8, self.header_height - 8 ]
      # pg.draw.rect(screen, Color.light_text, r1, 1)
      # w2 = self.header_cell_width * (end - k)
      # r2 = [ x + w1 + 4, 4, w2 - 8, self.header_height - 8 ]
      # pg.draw.rect(screen, Color.light_text, r2, 1)
      xy = [screen_size[0] // 2, self.header_height + 3 * FONT_SIZE]
      # temp = self.C[start][k] + self.C[k+1][end] + self.sizes[start-1]*self.sizes[k]*self.sizes[end]
      sizes, C = self.data.sizes, self.data.C
      total = C[start][k] + C[k+1][end] + sizes[start-1]*sizes[k]*sizes[end]
      text = (
        '%s × %s = ' % (self.result(start, k), self.result(k+1, end)) +
        'C[%d][%d] + C[%d+1][%d] + d[%d-1] × d[%d] × d[%d] = ' % (start, k, k, end, start, k, end) +
        self.result(start, k) + ' + ' + 
        self.result(k+1, end) + ' + ' +
        str(sizes[start-1]) + '×' + 
        str(sizes[k]) + '×' + 
        str(sizes[end]) + ' = ' +
        str(C[start][k]) + ' + ' +
        str(C[k+1][end]) + ' + ' +
        str(sizes[start-1] * sizes[k] * sizes[end]) + ' = ' +
        str(total)
      )
      self.draw_text(text, xy, Color.text)
      # print(rect)
      if start == k:
        sw, sh, sx, sy = self.cell_rect(start, start)
        self.draw_box([sx, sy, sw, sh], Color.pastel2[1], None)
      if end == k+1:
        sw, sh, sx, sy = self.cell_rect(end, end)
        self.draw_box([sx, sy, sw, sh], Color.pastel2[2], None)
      if total < C[start][end]:
        sw, sh, sx, sy = self.cell_rect(start, end)
        # pg.draw.circle(screen, Color.set1[0], [sx+sw//2, sy+sh//2], sh//2, 1)
        pg.draw.rect(screen, Color.set1[0], [sx+4, sy+4, sw-8,sh-8], 1)

      x = 3 * SEPARATOR_SIZE
      y = screen_size[1] - 3 * SEPARATOR_SIZE - 2 * FONT_SIZE
      self.draw_text('L=%d' % (self.sub_mult_count), [x, y], Color.set2[4], horz_center=False, font=bigFont)
      y += 2 * FONT_SIZE
      self.draw_text('s=%d e=%d' % (start, end), [x, y], Color.dark[4], horz_center=False, font=bigFont)
      if k >= 0:
        y += 2 * FONT_SIZE
        self.draw_text('k=%d' % k, [x, y], Color.set2[4], horz_center=False, font=bigFont)

  def draw_axis(self):
    sw, sh, sx, sy = self.cell_rect(1, 2)
    x, y = sx - SEPARATOR_SIZE // 2, sy + sh // 2
    for index in range(1, self.data.matrix_count):
      self.draw_text(str(index), [x, y], Color.light_text)
      y += sh

    x, y = sx + sw // 2, sy - FONT_SIZE
    for index in range(2, self.data.matrix_count + 1):
      self.draw_text(str(index), [x, y], Color.light_text)
      x += sw

  def cell_rect(self, start, end):
    sw = (screen_size[0] - 2 * SEPARATOR_SIZE) // (self.data.matrix_count - 1)
    sh = int((screen_size[1] - self.header_height - SEPARATOR_SIZE - 3 * FONT_SIZE) / (self.data.matrix_count - 0.7))
    sx = SEPARATOR_SIZE + (end - 2) * sw
    sy = self.header_height + SEPARATOR_SIZE + 3 * FONT_SIZE + (start - 1) * sh
    return sw, sh, sx, sy

  def on_mouse_motion(self):
    x, y = pg.mouse.get_pos()
    sw = (screen_size[0] - 2 * SEPARATOR_SIZE) // (self.data.matrix_count - 1)
    sh = int((screen_size[1] - self.header_height - SEPARATOR_SIZE - 3 * FONT_SIZE) / (self.data.matrix_count - 0.7))
    start = (y - self.header_height - SEPARATOR_SIZE - 3 * FONT_SIZE) // sh + 1
    end = (x - SEPARATOR_SIZE) // (sw) + 2
    if (1 <= start and start <= self.data.matrix_count and 
        2 <= end and end <= self.data.matrix_count):
      self.i_start, self.i_end = start, end
      self.i_k = self.data.P[start][end]
      if self.i_k == 0: self.i_k = -1
    else:
      self.i_start, self.i_end = -1, -1
      self.i_k = -1
    self.draw()

  def draw_c(self, start, end):
    sw, sh, sx, sy = self.cell_rect(start, end)
    # temp = self.C[start][k] + self.C[k+1][end] + self.sizes[start-1]*self.sizes[k]*self.sizes[end]
    pair = start, end
    if pair == (self.i_start, self.i_end):
      color = Color.pastel2[0]
    elif pair == (self.i_start, self.i_k):
      color = Color.pastel2[1]
    elif pair == (self.i_k+1, self.i_end):
      color = Color.pastel2[2]
    else:
      color = Color.back
    self.draw_box([sx, sy, sw, sh], color, Color.line)
    self.draw_text(str(self.data.C[start][end]), [sx+sw//2, sy+sh//2-FONT_SIZE//2], Color.text)
    self.draw_text(self.result(start, end), [sx+sw//2, sy+sh//2+FONT_SIZE//2], Color.dark[0])

  def draw_mini_matrix(self, index):
    y = self.header_height // 2
    w = self.data.matrix_count
    x = self.header_cell_width // 2 + index * self.header_cell_width
    row,col = self.data.sizes[index], self.data.sizes[index+1]
    rect = self.mini_rect(x, y, row, col)
    self.draw_box(rect, Color.pastel1[index], Color.set1[index])

    y = self.header_height * 4 // 5 + FONT_SIZE
    self.draw_text('%dx%d' % (row, col), [x, y], Color.text)
    self.draw_text('A%d' % (index+1), [x, FONT_SIZE], Color.text)

  def draw_adj_mult(self, index):
    x = index * self.header_cell_width
    y = self.header_height + FONT_SIZE
    row,common,col = self.data.sizes[index-1], self.data.sizes[index], self.data.sizes[index+1]
    self.draw_text('%dx%dx%d=%d' % (row, common, col, row*common*col), [x, y], Color.light_text)

  def mini_rect(self, center_x, center_y, row, col):
    rw = col * self.msize // self.max
    rh = row * self.msize // self.max
    return [ center_x - rw // 2, center_y - rh // 2, rw, rh]

def make_test_matrix(r, c, common):
  a = Matrix(r, common, rand=10)
  b = Matrix(common, c, rand=10)
  return a, b

def test_matrix_multiply():
  # a, b = make_test_matrix(2, 3, 2)
  # a, b = make_test_matrix(5, 6, 4)
  # a, b = make_test_matrix(2, 8, 3)
  a, b = make_test_matrix(6, 4, 8)
  c = Matrix(a.rows, b.cols)
  vis.setup(a, b, c)
  vis.draw()
  vis.start()
  # vis.update_display()

if __name__ == '__main__':
  vis = MatrixVisualizer('Matrix Test')
  test_matrix_multiply()
  vis.end()

