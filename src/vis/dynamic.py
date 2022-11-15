import math
from vis.base import *

class DictObject: 
  def __init__(self, **entries): 
    self.__dict__.update(entries)

class MatrixVisualizer(Visualizer):
  bctx_a = {
    'body_color': Color.pastel1[0],
    'line_color': Color.set1[0],
    'text_color': Color.text,
  }
  bctx_b = {
    'body_color': Color.pastel1[1],
    'line_color': Color.set1[1],
    'text_color': Color.text,
  }
  bctx_c = {
    'body_color': Color.pastel1[2],
    'line_color': Color.set1[2],
    'text_color': Color.text,
  }
  box_ctxs = [ bctx_a, bctx_b, bctx_c ]
  bctx_ha = {
    'body_color': Color.pastel2[0],
    'line_color': Color.set2[0],
    'text_color': Color.text,
  }
  bctx_hb = {
    'body_color': Color.pastel2[0],
    'line_color': Color.set2[1],
    'text_color': Color.text,
  }
  bctx_hc = {
    'body_color': Color.pastel2[2],
    'line_color': Color.set2[2],
    'text_color': Color.text,
  }
  hilight_ctxs = [ bctx_ha, bctx_hb, bctx_hc ]
  operator_color = Color.dark[0]
  operand_color = Color.dark[2]

  def setup(self, data):
    self.data = data

  def start(self, a, b, c):
    self.times = 0
    self.a, self.b, self.c = a, b, c
    self.matrixes = [a, b, c]
    self.idxs = [ 1, a.cols + 3, a.cols + b.cols + 5]
    self.cols = self.a.cols + self.b.cols + self.c.cols + 6
    self.rows = max(self.a.rows, self.b.rows, self.c.rows) + 2

  def update(self, row, col, idx):
    self.current_row = row
    self.current_col = col
    self.current_idx = idx
    self.times += 1
    self.draw(1000)

  def draw(self, wait_msec=0):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()
    if wait_msec > 0:
      self.wait(wait_msec)

  def calc_coords(self):
    self.cell_w = self.config.screen_width // self.cols
    self.cell_h = self.config.screen_height // self.rows

  def draw_content(self):
    for i in range(3):
      self.draw_matrix(self.matrixes[i], self.idxs[i], self.box_ctxs[i])
    self.draw_hilights()
    self.draw_others()

  def draw_hilights(self):
    self.draw_cell(0, self.current_row, self.current_idx)
    self.draw_cell(1, self.current_idx, self.current_col)
    self.draw_result_cell()

  def draw_cell(self, idx, row, col, shows_value=True):
    sx = int(self.idxs[idx] * self.cell_w)
    m = self.matrixes[idx]
    sy = (self.rows - m.rows) * self.cell_h // 2
    rect = [ 
      sx + col * self.cell_w, sy + row * self.cell_h,
      self.cell_w, self.cell_h
    ]
    text = str(self.matrixes[idx].data[row][col]) if shows_value else None
    ctx = self.hilight_ctxs[idx]
    self.draw_box(rect, text, **ctx)
    return rect

  def draw_result_cell(self):
    row, idx, col = self.current_row, self.current_idx, self.current_col
    x, y, w, h = self.draw_cell(2, row, col, False)
    x += w // 2
    y += (h - 3 * self.config.font_size) // 2
    mult_value = self.a.data[row][idx] * self.b.data[idx][col]
    sum_value = self.c.data[row][col]
    prev_value = sum_value - mult_value
    line_gap = self.config.font_size * 3 // 4

    self.draw_text(f'{prev_value}', [x, y], text_color=self.operand_color)
    y += line_gap
    self.draw_text('+', [x, y], text_color=self.operator_color)
    y += line_gap
    self.draw_text(f'{mult_value}', [x, y], text_color=self.operand_color)
    y += line_gap
    self.draw_text('=', [x, y], text_color=self.operator_color)
    y += line_gap
    self.draw_text(f'{sum_value}', [x, y])

  def draw_others(self):
    x = int((self.idxs[1] - 1) * self.cell_w)
    y = self.config.screen_height // 2
    self.draw_text('x', [x, y], Color.text, font=self.big_font)
    x = int((self.idxs[2] - 1) * self.cell_w)
    self.draw_text('=', [x, y], Color.text, font=self.big_font)

    xy = [self.cell_w, self.config.screen_height - 2 * self.config.font_size]
    self.draw_text('mult times = %d' % self.times, xy, center=False)

  def draw_matrix(self, m, xi, ctx):
    sx = int(xi * self.cell_w)
    sy = (self.rows - m.rows) * self.cell_h // 2

    mg = self.cell_w // 5
    box = [
      sx - mg, sy - mg, 
      m.cols * self.cell_w + 2 * mg,
      m.rows * self.cell_h + 2 * mg
    ]
    self.draw_box(box, **ctx)

    text = f'{m.rows} x {m.cols}'
    txy = [
      sx + m.cols * self.cell_w // 2, 
      sy - mg - self.config.font_size
    ]
    self.draw_text(text, txy, Color.text, font=self.big_font)

    sx += self.cell_w // 2
    y = sy + self.cell_h // 2
    for row in m.data:
      x = sx
      for v in row:
        self.draw_text(f'{v}', [x, y], Color.text)
        x += self.cell_w
      y += self.cell_h

class ChainedMatrixVisualizer(Visualizer):
  def setup(self, data):
    self.data = data

  def draw(self):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()