from vis.array import *
from vis.color import *
import math

class SortVisualizer(ArrayVisualizer):
  bctx_normal = {
    'body_color': Color.back,
    'line_color': Color.line,
    'text_color': Color.text,
    'no_body': True
  }
  bctx_compare = {
    'body_color': Color.LightSalmon,
    'line_color': Color.DarkRed,
    'text_color': Color.Indigo,
  }
  bctx_swap1 = {
    'body_color': Color.PaleGreen,
    'line_color': Color.DarkOliveGreen,
    'text_color': Color.DarkGreen,
  }
  bctx_swap2 = {
    'body_color': Color.LightSkyBlue,
    'line_color': Color.DarkBlue,
    'text_color': Color.MidnightBlue,
  }
  bctx_fixed = {
    'body_color': Color.Gainsboro,
    'line_color': Color.Gray,
    'text_color': Color.DarkSlateGray,
  }

  def setup(self, data):
    self.data = data
    self.item_contexts = dict()
    self.compare_i1, self.compare_i2 = -1, -1
    self.swap_i1, self.swap_i2 = -1, -1
    self.compare_count = 0
    self.swap_count = 0

  def get_item_context(self, index):
    if index in self.item_contexts:
      return self.item_contexts[index]
    return None

  def set_item_context(self, index, context=None):
    if context == None:
      if index in self.item_contexts:
        del self.item_contexts[index]
      return
    self.item_contexts[index] = context

  def draw_cell(self, index):
    ctx = self.get_item_context(index)
    if not ctx: ctx = self.bctx_normal

    rect = self.get_rect(index)
    # print(index, ctx)
    self.draw_box(rect, text=str(self.data.array[index]), **ctx)

  def compare(self, i1, i2):
    self.compare_count += 1
    self.compare_i1, self.compare_i2 = i1, i2
    self.set_compare_context(i1, i2, True)
    self.draw()
    self.draw_compare_text()
    self.update_display()
    self.wait(1000)
    self.set_compare_context(i1, i2, False)
    self.compare_i1, self.compare_i2 = -1, -1

  def set_compare_context(self, i1, i2, on):
    ctx = self.bctx_compare if on else None
    self.set_item_context(i1, ctx)
    self.set_item_context(i2, ctx)

  def draw_compare_text(self):
    if self.compare_i1 < 0: return
    rect = self.get_rect(self.compare_i1)
    rect[1] += rect[3]
    rect[3] = 2 * self.config.font_size
    xy = rect_center(rect)
    v1, v2 = self.get_compare_values()
    shouldSwap = v1 > v2
    font = self.big_font if shouldSwap else self.small_font
    op = '>' if shouldSwap else '<='
    self.draw_text(f'{v1} {op} {v2}', xy, font=font)
    # print(f'{v1=} {op=} {v2=} {xy=}')

  def get_compare_values(self):
     return self.data.array[self.compare_i1], self.data.array[self.compare_i2]

  def swap(self, i1, i2):
    self.swap_count += 1
    self.swap_i1, self.swap_i2 = i1, i2
    self.set_item_context(i1, self.bctx_swap1)
    self.set_item_context(i2, self.bctx_swap2)
    self.animate(1000)
    self.set_item_context(i1)
    self.set_item_context(i2)
    self.swap_i1, self.swap_i2 = -1, -1

  def draw_content(self):
    super().draw_content()
    self.draw_counts()

  def draw_counts(self):
    text = \
      f'Data Length = {len(self.data.array)}\n' \
      f'Comparison = {self.compare_count}\n' \
      f'Swap = {self.swap_count}'
    xy = self.separator_size, self.separator_size
    self.draw_text(text, xy, center=False)

  def get_rect(self, index):
    x = self.separator_size + index * self.cell_w 
    rect = [x, self.table_y, self.cell_w, self.cell_w]
    if index == self.swap_i1:
      ox, oy = self.anim_offset(index, self.swap_i2)
      rect[0] += ox
      rect[1] += oy
    elif index == self.swap_i2:
      ox, oy = self.anim_offset(index, self.swap_i1)
      rect[0] += ox
      rect[1] += oy
    return rect

  def anim_offset(self, i1, i2):
    dx = (i2-i1) * self.cell_w
    dy = (1 if i1-i2 > 0 else -1) * self.cell_w

    ox = dx * self.anim_progress
    oy = dy * (-2 * (self.anim_progress - 0.5) ** 2 + 0.5)

    return ox, oy


class BubbleSortVisualizer(SortVisualizer):
  def __init__(self, title):
    super().__init__(title)

  def bubble_end(self, end):
    if end >= len(self.data.array): return
    self.set_item_context(end, self.bctx_fixed)
    self.draw()

class SelectionSortVisualizer(SortVisualizer):
  def setup(self, data):
    super().setup(data)
    self.selected_index = -1

  def selection(self, index):
    self.selected_index = index

  def draw_content(self):
    super().draw_content()
    self.draw_selection_mark()

  def draw_selection_mark(self):
    if self.selected_index < 0: return
    rect = self.get_rect(self.selected_index)
    rect[1] -= self.separator_size
    rect[3] = self.separator_size
    xy = rect_center(rect)
    self.draw_text('min@', xy, font=self.big_font)

  def mark_done(self, index):
    self.set_item_context(index, self.bctx_fixed)
    self.selected_index = -1
    self.draw()
    self.wait(1000)

class InsertionSortVisualizer(SortVisualizer):
  bctx_shift = {
    'body_color': Color.Violet,
    'line_color': Color.line,
    'text_color': Color.text,
  }
  bctx_picked = {
    'body_color': Color.Pink,
    'line_color': Color.MediumVioletRed,
    'text_color': Color.text,
  }
  bctx_cmp_will_shift = {
    'body_color': Color.MediumPurple,
    'line_color': Color.line,
    'text_color': Color.text,
  }
  bctx_cmp_wont_shift = {
    'body_color': Color.LightSlateGray,
    'line_color': Color.line,
    'text_color': Color.text,
  }
  bctx_same_line = {
    'body_color': Color.Linen,
    'line_color': Color.line,
    'text_color': Color.text,
  }

  def setup(self, data):
    super().setup(data)
    self.end_index = -1
    self.shows_pick = False
    self.animates_pick = False
    self.pick_value = None

    self.mmm = '//'

  def mark_end(self, index, pick=False):
    self.end_index = index
    if pick:
      self.shows_pick = True
      self.pick_value = self.data.array[index]
      self.swap_count += 1
    self.draw()
    self.wait(1000)

  def get_item_context(self, index):
    ctx = super().get_item_context(index)
    if ctx: return ctx

    if index <= self.end_index:
      return self.bctx_fixed

    return self.bctx_same_line

  def draw_content(self):
    self.draw_sorted_range()
    super().draw_content()
    self.draw_animating_box()

  def draw_sorted_range(self):
    fs = self.config.font_size
    rx,y,_,h = self.get_rect(self.end_index)
    x = self.separator_size - fs
    y -= fs
    w = rx - x + fs + self.cell_w
    h += 2 * fs
    rect = [x, y, w, h]
    pg.draw.rect(self.screen, Color.Beige, rect)

  def shift(self, i1, i2, pick=False):
    self.animates_pick = pick
    self.anim_value = self.data.array[i1]
    self.swap_count += 1
    self.swap_i1, self.swap_i2 = i1, i2
    self.animate(1000)
    self.swap_i1, self.swap_i2 = -1, -1
    if pick: 
      self.shows_pick = False
      self.animates_pick = False

  def draw_animating_box(self):
    if not self.shows_pick: return
    if self.end_index < 0: return

    rect = self.get_rect(self.end_index)
    # print(f'{self.end_index=} {rect=}')
    if self.animates_pick:
      ox = self.anim_progress * (self.swap_i2-self.swap_i1) * self.cell_w
      oy = (1 - self.anim_progress) * self.cell_w
      rect[0] += ox
      rect[1] -= oy
    else:
      rect[1] -= rect[3]
    self.draw_box(rect, str(self.pick_value), **self.bctx_picked)

    if not self.animates_pick:
      if self.swap_i1 >= 0:
        rect = self.get_rect(self.swap_i1)
        dx = (self.swap_i2-self.swap_i1) * self.cell_w
        ox = dx * self.anim_progress
        rect[0] += ox
        self.draw_box(rect, str(self.anim_value), **self.bctx_shift)

  def get_rect(self, index):
    if self.shows_pick:
      return ArrayVisualizer.get_rect(self, index)
    else:
      return SortVisualizer.get_rect(self, index)

  def get_compare_values(self):
    if self.pick_value is None:
      return self.data.array[self.compare_i1], self.data.array[self.compare_i2]
    return self.data.array[self.compare_i1], self.pick_value

  def set_compare_context(self, i1, i2, on):
    # print(f'{i1=} {i2=} {on=}')
    if on:
      v1, v2 = self.get_compare_values()
      if v1 > v2:
        ctx = self.bctx_cmp_will_shift
      else:
        ctx = self.bctx_cmp_wont_shift
    else:
      ctx = None
    # ctx = self.bctx_compare if on else None
    self.set_item_context(i1, ctx)
    # self.set_item_context(i2, ctx)

class ShellSortVisualizer(InsertionSortVisualizer):
  bctx_outof_interest = {
    'body_color': Color.back,
    'line_color': Color.Gray,
    'text_color': Color.Gray,
    'no_body': True
    }
  def setup(self, data):
    super().setup(data)
    self.gap = 1
    self.prev_gap = -1

  def set_gap(self, gap):
    self.prev_gap = self.gap if gap < self.gap else -1
    self.gap = gap
    if self.prev_gap < 0: return

    self.animate(1000)
    self.prev_gap = -1

  def calc_coords(self):
    super().calc_coords()
    self.space_h = (self.config.screen_height 
      - self.table_y - self.separator_size - self.cell_w)
    # gap = self.gap
    # if self.gap_diff > 0:
    #   gap += (1.0 - self.anim_progress) * self.gap_diff
    # self.gap_h = int(space / gap)
    # print(f'{gap=}')

  def get_rect(self, index):
    rect = super().get_rect(index)
    y = index % self.gap
    gap_h = self.space_h // self.gap
    diff = y * gap_h
    if self.prev_gap > 0:
      gy = index % self.prev_gap
      gh = self.space_h // self.prev_gap
      py = gy * gh
      diff += (py - diff) * (1.0 - self.anim_progress)
    # print(f'{index=} {rect=} {y=} {self.gap_h=} {self.gap=}')
    rect[1] += diff
    return rect

  def get_item_context(self, index):
    ctx = SortVisualizer.get_item_context(self, index)
    if ctx: return ctx

    same_line = index % self.gap == self.end_index % self.gap
    if same_line:
      if index <= self.end_index:
        return self.bctx_fixed
      else: 
        return self.bctx_same_line

    return self.bctx_outof_interest

class HeapSortVisualizer(SortVisualizer):
  nctx_normal = {
    'body_color': Color.back,
    # 'line_color': Color.line,
    # 'text_color': Color.text,
    # 'width': 3,
  }
  bctx_subtree_good = {
    'body_color': Color.AliceBlue,
    'line_color': Color.DodgerBlue,
    # 'text_color': Color.text,
  }
  bctx_subtree_bad = {
    'body_color': Color.MistyRose,
    'line_color': Color.LightCoral,
    # 'text_color': Color.text,
  }
  clr_good_child = Color.Lime
  clr_bad_child = Color.Crimson

  def setup(self, data):
    super().setup(data)
    self.building_tree = False
    self.root_index = -1
    self.tree_size = len(self.data.array)

  def build_tree(self):
    self.building_tree = True
    self.animate(1000)
    self.building_tree = False

  def set_root(self, root=-1):
    if self.root_index >= 0:
      self.draw()
      self.wait(1000)
    self.root_index = root
    self.draw()
    self.wait(1000)

  def set_tree_size(self, size=0):
    self.tree_size = size
    self.set_item_context(size, self.bctx_fixed)
    self.draw()
    self.wait(1000)

  def calc_coords(self):
    super().calc_coords()
    sep = self.separator_size
    self.table_y = self.config.screen_height - sep - self.cell_w

    l_arr = len(self.data.array)
    self.tree_x = sep
    self.tree_width = self.config.screen_width - 2 * sep
    self.row_cell_h = max(self.cell_w, self.config.screen_height // 10)
    self.tree_max_level = math.ceil(math.log2(l_arr + 1))
    self.node_radius = max(self.cell_w, self.config.font_size) // 2
    self.tree_height = self.row_cell_h * self.tree_max_level
    self.tree_y = self.table_y - sep - self.tree_height
    # self.tree_height = self.table_y - sep - self.tree_y
    # self.row_cell_h = self.tree_height // self.tree_max_level

  def draw_content(self):
    self.draw_root_boundary()
    super().draw_content()
    self.draw_tree()

  def draw_root_boundary(self):
    index = self.root_index
    if index < 0: return

    y_idx = math.ceil(math.log2(index+2)) - 1
    node_in_y_row = 2 ** y_idx
    x_idx = index - node_in_y_row + 1

    subtree_w = self.tree_width // node_in_y_row
    subtree_h = (self.tree_max_level - y_idx) * self.row_cell_h
    subtree_x = self.tree_x + x_idx * subtree_w
    subtree_y = self.tree_y + y_idx * self.row_cell_h

    fs = self.config.font_size
    rect = [
      subtree_x - fs, subtree_y - fs, 
      subtree_w + 2*fs, subtree_h + 2*fs
    ]
    ctx = self.bctx_subtree_good if self.isHeap(index) else self.bctx_subtree_bad
    self.draw_box(rect, border_radius=self.node_radius, **ctx)

  def isHeap(self, index):
    count = self.tree_size

    lc = index * 2 + 1
    if lc >= count: return True
    my_value = self.data.array[index]
    ch_value = self.data.array[lc]
    if my_value < ch_value: return False

    if not self.isHeap(lc): return False

    rc = index * 2 + 2
    if rc >= count: return True
    ch_value = self.data.array[rc]
    if my_value < ch_value: return False

    if not self.isHeap(rc): return False

    return True

  def draw_tree(self):
    for i in range(len(self.data.array)):
      self.draw_tree_edge(i, i*2+1)
      self.draw_tree_edge(i, i*2+2)
    for i in range(len(self.data.array)):
      self.draw_tree_node(i)

  def draw_tree_node(self, index):
    ctx = self.get_item_context(index)
    if not ctx: ctx = self.nctx_normal

    xy = self.get_tree_node_pos(index)
    self.draw_circle(xy, self.node_radius, str(self.data.array[index]), **ctx)

  def draw_tree_edge(self, pi, ci):
    if ci >= self.tree_size: return
    # check end here
    pxy = self.get_tree_node_pos(pi, False)
    cxy = self.get_tree_node_pos(ci, False)
    pv = self.data.array[pi]
    cv = self.data.array[ci]
    if pv >= cv:
      color = self.clr_good_child
    else:
      color = self.clr_bad_child
    pg.draw.line(self.screen, color, pxy, cxy, 3)

  def get_tree_node_pos(self, index, apply_swap=True):
    y_idx = math.ceil(math.log2(index+2)) - 1
    node_in_y_row = 2 ** y_idx
    x_idx = index - node_in_y_row + 1

    cell_w = self.tree_width // node_in_y_row
    cell_h = self.row_cell_h
    nx = self.tree_x + x_idx * cell_w + cell_w // 2
    ny = self.tree_y + y_idx * cell_h + cell_h // 2

    if self.building_tree:
      rect = self.get_rect(index)
      x,y = rect_center(rect)
      nx += (x - nx) * (1-self.anim_progress)
      ny += (y - ny) * (1-self.anim_progress)

    if not apply_swap:
      return nx, ny

    if index == self.swap_i1:
      ox, oy = self.anim_node_offset(nx, ny, self.swap_i2)
      # print(f'{index=} {nx=},{ny=} {nx=},{ny=} {ox=:.2f},{oy=:.2f}')
      nx += ox
      ny += oy
    elif index == self.swap_i2:
      ox, oy = self.anim_node_offset(nx, ny, self.swap_i1)
      nx += ox
      ny += oy
    return nx, ny

  def anim_node_offset(self, x, y, target):
    tx, ty = self.get_tree_node_pos(target, False)
    # ty = y - 200
    dx, dy = tx - x, ty - y
    angle = math.atan2(dy, dx)
    dist = math.sqrt(dx**2+dy**2)
    prog = self.anim_progress
    px = prog * dist
    py = (-2 * (prog - 0.5) ** 2 + 0.5) * self.node_radius * 2
    ox = px * math.cos(angle) + py * math.sin(angle)
    oy = px * math.sin(angle) - py * math.cos(angle)

    return ox, oy

class CountSortVisualizer(ArrayVisualizer):
  bctx_index = {
    'line_color': Color.LightGray,
    'text_color': Color.LightGray,
    'no_body': True
  }
  bctx_item = {
    'body_color': Color.Cornsilk,
    'line_color': Color.line,
    'text_color': Color.Navy,
  }
  bctx_item_now = {
    'body_color': Color.BurlyWood,
    'line_color': Color.line,
    'text_color': Color.text,
  }
  bctx_item_fixed = {
    'body_color': Color.Ivory,
    'line_color': Color.line,
    'text_color': Color.RoyalBlue,
  }
  bctx_count = {
    'body_color': Color.Azure,
    'line_color': Color.line,
    'text_color': Color.line,
    # 'no_body': True
  }
  bctx_count_inc = {
    'body_color': Color.DeepSkyBlue,
    'line_color': Color.line,
    'text_color': Color.Brown,
    # 'no_body': True
  }
  def __init__(self, title):
    super().__init__(title)

  def setup(self, data):
    self.data = data
    self.inc_index = -1
    self.increasing = True
    self.anim_type = 0

    l_arr = len(self.data.array)
    self.l_counts = 20 if l_arr < 80 else 30
    self.items_in_a_row = self.l_counts

  def set_inc_index(self, index, increasing=True):
    self.inc_index = index
    self.increasing = increasing

    self.anim_type = 1 if increasing else 2
    self.animate(500)
    self.anim_type = 0

  def calc_coords(self):
    sep = self.separator_size
    self.pane_w = (self.config.screen_width - 2 * sep)
    self.count_w = self.pane_w // self.l_counts
    self.count_y = (self.config.screen_height - self.count_w) // 2
    self.pane_h = self.count_y - 2 * sep
    self.pane_x = sep
    self.upper_pane_y = sep
    self.lower_pane_y = self.count_y + self.count_w + sep
    self.item_w = self.pane_w // self.items_in_a_row
    # count = len(self.data.array)
    # print(self.__dict__)

  def draw_content(self):
    if hasattr(self.data, 'counts'):
      self.draw_counts()

    self.draw_pane(True, self.data.array)

    if hasattr(self.data, 'result'):
      self.draw_pane(False, self.data.result)

  def animates_count(self, index):
    return self.inc_index >= 0 and index == self.data.array[self.inc_index]

  def draw_counts(self):
    for i in range(len(self.data.counts)):
      count = self.data.counts[i]
      rect = [
        self.pane_x + i * self.count_w, 
        self.count_y, self.count_w, self.count_w
      ]
      value = self.data.array[self.inc_index]
      animates = self.animates_count(i)
      if animates:
        ctx = self.bctx_count_inc
      else:
        ctx = self.bctx_count

      x,y = rect_center(rect)
      if self.anim_type > 0 and animates:
        sign = -1 if self.anim_type == 1 else 1
        # print(f'{self.anim_type=} {sign=} {i=}')
        self.draw_box(rect, **ctx)
        ch = rect[3]
        self.clip(rect)
        ay = y + sign * ch * self.anim_progress
        self.draw_text(str(count + sign), [x, ay], **self.bctx_item)
        ay -= sign * ch
        self.draw_text(str(count), [x, ay], **self.bctx_item)
        self.clip(None)
      else:
        self.draw_box(rect, str(count), **ctx)

      # x = rect[0] + rect[2]//2
      y = rect[1] - self.config.font_size
      self.draw_text(str(i), [x,y], **self.bctx_item)

  def get_pane_pos(self, isUpper):
    x = self.pane_x
    y = self.upper_pane_y if isUpper else self.lower_pane_y
    return x, y

  def draw_pane(self, isUpper, array):
    for i in range(len(array)):
      self.draw_item(isUpper, array, i, False)
    for i in range(len(array)):
      if array[i] != None:
        self.draw_item(isUpper, array, i, True)

  def draw_item(self, isUpper, array, index, vivid):
    if vivid:
      swap = True
      text = str(array[index])
      ctx = self.bctx_item_fixed
      if isUpper:
        if index == self.inc_index:
          ctx = self.bctx_item_now
        elif index < self.inc_index:
          ctx = self.bctx_item
    else:
      swap = False
      text = str(index)
      ctx = self.bctx_index
      # print(f'{isUpper=} {self.increasing=} {self.inc_index=}')
      if not isUpper and not self.increasing and self.inc_index >= 0:
        value = self.data.array[self.inc_index]
        at = self.data.counts[value]
        if index == at:
          ctx = self.bctx_count_inc

    rect = self.get_item_rect(isUpper, index, swap)
    self.draw_box(rect, text, **ctx)

  def get_item_rect(self, isUpper, index, apply_swap=True):
    px, py = self.get_pane_pos(isUpper)
    sep = self.separator_size
    iw = self.item_w
    x = px + iw * (index % self.items_in_a_row)
    y = py + iw * (index // self.items_in_a_row)
    # print(f'{isUpper=} {index=} {px=},{py=} {x=},{y=}')
    return [x, y, iw, iw]

class RadixSortLsdVisualizer(CountSortVisualizer):
  def set_inc_index(self, div, index, increasing=True):
    super().set_inc_index(index, increasing)
    self.radix_div = div

  def animates_count(self, index):
    if not hasattr(self, 'radix_div'): return False
    return self.inc_index >= 0 and index == (self.data.array[self.inc_index] // self.radix_div % 10)
