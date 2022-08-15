from vis.base import *

clr = Color()
clr.compare = Color.pastel2[0]
clr.max = Color.pastel2[1]

class ArrayVisualizer(Visualizer):
  def setup(self, data):
    self.data = data
    self.draw()

  def draw_content(self):
    self.calc_coords()
    self.draw_table()

  def calc_coords(self):
    self.cell_w = (self.config.screen_width - 2 * self.separator_size) // len(self.data.array)
    if self.cell_w > 150: self.cell_w = 150

    self.table_y = self.config.screen_height * 2 // 5

  def draw_table(self):
    for i in range(len(self.data.array)):
      self.draw_cell(i)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    self.draw_box(rect, text=str(self.data.array[index]))

  def get_rect(self, index):
    x = self.separator_size + index * self.cell_w 
    return [x, self.table_y, self.cell_w, self.cell_w]

class FindMaxVisualizer(ArrayVisualizer):
  def setup(self, data):
    self.max_index = -1
    self.compare_index = -1
    super().setup(data)

  def compare(self, index):
    self.compare_index = index
    self.draw()
    self.wait(1000)

  def update(self):
    self.max_index = self.compare_index
    self.draw()
    self.wait(1000)

  def draw_content(self):
    super().draw_content()
    if self.max_index >= 0:
      rect = self.get_rect(self.max_index)
      rect[1] -= self.separator_size
      rect[3] = self.separator_size
      self.draw_box(rect, f'@{self.max_index}', no_line=True, no_body=True, font=self.big_font)
    if self.compare_index >= 0:
      rect = self.get_rect(self.compare_index)
      rect[1] += rect[3]
      rect[3] = self.separator_size

      value = self.data.array[self.compare_index]
      max = self.data.array[self.max_index] if self.max_index >= 0 else float('-inf')
      if value > max:
        text = f'{value} > {max}'
        font = self.big_font
      elif value < max:
        text = f'{value} < {max}'
        font = self.small_font
      else:
        text = f'{value} == {max}'
        font = self.small_font
      self.draw_box(rect, text, no_line=True, no_body=True, font=font)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    if index == self.max_index:
      color = clr.max
    elif index == self.compare_index:
      color = clr.compare
    else:
      color = clr.back
    self.draw_box(rect, text=str(self.data.array[index]), body_color=color)

class SearchVisualizer(ArrayVisualizer):
  def setup(self, data):
    self.found_index = -1
    self.compare_index = -1
    super().setup(data)

  def compare(self, index):
    self.compare_index = index
    self.draw()
    self.wait(1000)

  def update(self):
    self.found_index = self.compare_index
    self.draw()
    self.wait(1000)

  def draw_content(self):
    super().draw_content()
    if self.found_index >= 0:
      rect = self.get_rect(self.found_index)
      rect[1] -= self.separator_size
      rect[3] = self.separator_size
      self.draw_box(rect, f'@{self.found_index}', no_line=True, no_body=True, font=self.big_font)
    else:
      xy = self.separator_size, self.separator_size
      self.draw_text(f'{self.data.to_find} Not Found', xy, center=False, font=self.big_font)
    if self.compare_index >= 0:
      rect = self.get_rect(self.compare_index)
      rect[1] += rect[3]
      rect[3] = self.separator_size

      value = self.data.array[self.compare_index]
      if value == self.data.to_find:
        text = f'{value} == {self.data.to_find}'
        font = self.big_font
      else:
        text = f'{value} != {self.data.to_find}'
        font = self.small_font
      self.draw_box(rect, text, no_line=True, no_body=True, font=font)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    if index == self.found_index:
      color = clr.max
    elif index == self.compare_index:
      color = clr.compare
    else:
      color = clr.back
    self.draw_box(rect, text=str(self.data.array[index]), body_color=color)

