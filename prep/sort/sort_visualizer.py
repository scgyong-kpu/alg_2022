import pygame as pg
import math

screen_size = [ 1600, 900 ]
BACK_COLOR = ( 255, 255, 255 )
EDGE_COLOR = ( 0, 63, 0 )
TEXT_COLOR = ( 0, 0, 63 )
COMPARE_COLOR = (251,180,174)
SELECTION_COLOR = (229,216,189)
SWAP_COLOR_1 = (179,205,227)
SWAP_COLOR_2 = (204,235,197)
MERGED_COLOR = (222,203,228)
MERGE_LEFT_COLOR = (254,217,166)
MERGE_RIGHT_COLOR = (229,216,189)
QUICK_FIXED_COLOR = (242,242,242)
EDGE_GOOD_COLOR = (55,126,184)
EDGE_BAD_COLOR = (166,86,40)
HEAP_ROOT_COLOR = (152,78,163)
HEAP_CURR_ROOT_COLOR = (253,218,236)
WAIT_ONE_FRAME_MILLIS = 15
WAIT_COMPARE_MILLIS_1 = 700
WAIT_COMPARE_MILLIS_2 = 100
WAIT_SWAP_ANIM_MILLIS = 1000
WAIT_SWAP_SHOW_MILLIS = 300
WAIT_MERGE_MILLIS = 300
WAIT_QUICK_SET_MILLIS = 300
WAIT_QUICK_PIVOT_MILLIS = 500
# ["#fbb4ae","#b3cde3","#ccebc5","#decbe4","#fed9a6","#ffffcc","#e5d8bd","#fddaec","#f2f2f2"]
# (251,180,174)
# (179,205,227)
# (204,235,197)
# (222,203,228)
# (254,217,166)
# (255,255,204)
# (229,216,189)
# (253,218,236)
# (242,242,242)

# ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33","#a65628","#f781bf","#999999"]
# (228,26,28)
# (55,126,184)
# (77,175,74)
# (152,78,163)
# (255,127,0)
# (255,255,51)
# (166,86,40)
# (247,129,191)
# (153,153,153)

speed = 1
partitions = []
max_partition = 0
quick = False
selection = False


def init(title):
  global screen
  pg.init()
  screen = pg.display.set_mode(screen_size)
  pg.display.set_caption(title)
  clear()

def clear(color = (255,255,255)):
  screen.fill(color)

def wait(millis):
  millis = int(millis / speed)
  if millis < WAIT_ONE_FRAME_MILLIS: millis = WAIT_ONE_FRAME_MILLIS

  pg.time.wait(millis)
  loop = True
  first = True
  while loop:
    if first:
      first = False
      loop = False
    for e in pg.event.get():
      if e.type == pg.QUIT:
        pg.quit()
      elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
        pg.quit()
      elif e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
        loop = True
      elif e.type == pg.KEYUP and e.key == pg.K_SPACE:
        loop = False

def wait_for_keydown():
  loop = True
  while loop:
    for e in pg.event.get():
      if e.type == pg.QUIT:
        loop = False
        pg.quit()
      elif e.type == pg.KEYDOWN:
        loop = False

def end():
  loop = True
  while loop:
    for e in pg.event.get():
      if e.type == pg.QUIT:
        loop = False
      elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
        loop = False
  pg.quit()

def setup(list):
  global the_array
  the_array = list

  clear(BACK_COLOR)
  global unit, count, base_y
  sw = screen_size[0]
  count = len(list)

  unit = sw // count
  if unit < 10:
    raise Exception('List too large')
  if unit > 150:
    unit = 150

  hu = unit // 2

  base_y = screen_size[1] // 2 - unit

  global font, font_size, font_height
  font_size = unit // 3
  if font_size > 50: font_size = 50
  if font_size < 10: font_size = 10
  font_height = font_size * 4 // 3
  font = pg.font.SysFont("arial", font_size)
  print('unit:', unit, 'font_size:', font_size)

  y1 = base_y
  y2 = y1 + unit
  xe = unit * count
  pg.draw.line(screen, EDGE_COLOR, [0, y1], [xe, y1])
  pg.draw.line(screen, EDGE_COLOR, [0, y2], [xe, y2])
  x = 0
  for i in range(count):
    pg.draw.line(screen, EDGE_COLOR, [x, y1], [x, y2])
    draw_text(font, str(list[i]), [x+hu, y1+hu], TEXT_COLOR)
    x += unit
  pg.draw.line(screen, EDGE_COLOR, [x, y1], [x, y2])

  pg.display.flip()

def draw_text(font, text, xy, color, horz_center = True):
  img = font.render(text, True, color)
  if (horz_center):
    rect = img.get_rect(center = xy)
    screen.blit(img, rect)
  else:
    screen.blit(img, xy)

def selection(list = None, start = None, min = None, count = None):
  sw = screen_size[0]
  y = base_y - font_height
  pg.draw.rect(screen, BACK_COLOR, [0, y, sw, font_height])
  if list == None: return
  x = start * unit
  if count == None: count = len(list)
  w = count * unit - x
  pg.draw.rect(screen, SELECTION_COLOR, [x, y, w, font_height - 1])
  annotation(1, min, 'v')

def bubble(list, start, comp, mid, end):
  y = base_y - font_height
  x = start * unit
  w = (mid - start) * unit
  pg.draw.rect(screen, SELECTION_COLOR, [x, y, w, font_height - 1])
  if start > 0:
    x = 0
    w = start * unit
    pg.draw.rect(screen, QUICK_FIXED_COLOR, [x, y, w, font_height - 1])
  if mid < end:
    x = mid * unit
    w = (end - mid) * unit
    pg.draw.rect(screen, QUICK_FIXED_COLOR, [x, y, w, font_height - 1])

  if comp != None:
    annotation(1, comp, 'v')
  else:
    pg.display.flip()

def insertion_init(list, index):
  draw_elem(list, index, SWAP_COLOR_1, level=1)
  pg.display.flip()
  wait(WAIT_SWAP_SHOW_MILLIS)

def insertion_move(list, i1, i2, value=None):
  if value == None:
    v = list[i1]
    level = 0
  else:
    v = value
    level = 1
  y1 = base_y
  y2 = y1 + unit
  x1, x2 = i1 * unit, i2 * unit
  v1, v2 = list[i1], list[i2]
  diff = x1 - x2
  frames = int(WAIT_SWAP_ANIM_MILLIS / 2 / speed) // WAIT_ONE_FRAME_MILLIS
  if frames < 2: frames = 2
  for i in range(frames + 1):
    xx1 = x1 - diff * i // frames
    if level > 0: 
      erase_level(level)
    else:
      draw_elem(list, i1, BACK_COLOR)
      xx2 = xx1 + unit
      pg.draw.line(screen, EDGE_COLOR, [xx1, y1], [xx1, y2])
      pg.draw.line(screen, EDGE_COLOR, [xx2, y1], [xx2, y2])
    color = SWAP_COLOR_2 if value == None else SWAP_COLOR_1
    draw_elem(list, 0, color, level=level, value=v, x=xx1)
    pg.display.flip()
    wait(WAIT_ONE_FRAME_MILLIS)
  wait(WAIT_SWAP_SHOW_MILLIS)

  if value != None: 
    erase_level(1)

  draw_elem(list, i2, BACK_COLOR, value=v)
  # print(level, i2, value)
  pg.display.flip()

def compare(list, i1, i2):
  for n in range(1):
    draw_elem(list, i1, COMPARE_COLOR)
    draw_elem(list, i2, COMPARE_COLOR)
    pg.display.flip()
    wait(WAIT_COMPARE_MILLIS_1)

    draw_elem(list, i1, BACK_COLOR)
    draw_elem(list, i2, BACK_COLOR)
    pg.display.flip()
    wait(WAIT_COMPARE_MILLIS_2)

def swap(list, i1, i2):
  draw_elem(list, i1, SWAP_COLOR_1)
  draw_elem(list, i2, SWAP_COLOR_2)
  draw_elem(list, i1, SWAP_COLOR_1, level=1)
  draw_elem(list, i2, SWAP_COLOR_2, level=1)
  pg.display.flip()
  wait(WAIT_SWAP_SHOW_MILLIS)
  x1, x2 = i1 * unit, i2 * unit
  v1, v2 = list[i1], list[i2]
  diff = x1 - x2
  frames = int(WAIT_SWAP_ANIM_MILLIS / speed) // WAIT_ONE_FRAME_MILLIS
  if frames < 2: frames = 2
  for i in range(frames + 1):
    erase_level(1)
    xx1 = x1 - diff * i // frames
    xx2 = x2 + diff * i // frames
    draw_elem(list, 0, SWAP_COLOR_1, level=1, value=v1, x=xx1)
    draw_elem(list, 0, SWAP_COLOR_2, level=1, value=v2, x=xx2)
    pg.display.flip()
    wait(WAIT_ONE_FRAME_MILLIS)
  wait(WAIT_SWAP_SHOW_MILLIS)
  draw_elem(list, i1, SWAP_COLOR_2, value=v2)
  draw_elem(list, i2, SWAP_COLOR_1, value=v1)
  erase_level(1)
  pg.display.flip()
  wait(WAIT_SWAP_SHOW_MILLIS)
  draw_elem(list, i1, BACK_COLOR, value=v2)
  draw_elem(list, i2, BACK_COLOR, value=v1)
  pg.display.flip()

def erase_level(level):
  y1 = base_y + int(level * unit)
  sw = screen_size[0]
  rect = [0, y1+1, sw, unit-1]
  pg.draw.rect(screen, BACK_COLOR, rect)


def draw_elem(list, index, color, level = 0, value = None, x = None):
  if value == None:
    text = str(list[index])
  else:
    text = str(value)
  if x == None:
    x = index * unit
  y1 = base_y + level * unit
  rect = [x + 1, y1 + 1, unit - 1, unit - 1]
  pt = [x + unit // 2, y1 + unit // 2]
  # print(index, rect, pt, color)
  pg.draw.rect(screen, color, rect)
  draw_text(font, text, pt, TEXT_COLOR)

def annotation(level, index, text = ''):
  y1 = base_y - int(level * font_height)
  x = int(index * unit)
  if text == '':
    pg.draw.rect(screen, BACK_COLOR, [x, y1, unit, font_height])
  if text != '': 
    adj = font_size // 8
    draw_text(font, text, [x + unit // 2, y1 + font_height // 2 - adj], TEXT_COLOR)
  pg.display.flip()

def erase_annotation(level):
  y1 = base_y - int(level * font_height)
  sw = screen_size[0]
  pg.draw.rect(screen, BACK_COLOR, [0, y1, sw, font_height])

def partition_push(p, m, q):
  global max_partition
  partitions.append((p, m, q))
  size = len(partitions)
  if max_partition < size:
    max_partition = size
  partition_show()
  wait(300)

def partition_pop():
  partitions.pop()
  partition_show()
  wait(300)

def partition_show():
  eh = max_partition * font_height
  sw = screen_size[0]
  pg.draw.rect(screen, BACK_COLOR, [0, base_y - eh, sw, eh])

  draw_level = quicksort_draw_level if quick else partition_draw_level
  for i in range(len(partitions)):
    draw_level(i)

  pg.display.flip()

def partition_draw_level(index):
  level = len(partitions) - index
  y = base_y - level * font_height
  p, m, q = partitions[index]

  px = p * unit
  qx = (q + 1) * unit
  mx = (m + 1) * unit
  # if p == m: mx += unit // 5
  # if m == q: mx = qx - unit // 5
  pg.draw.rect(screen, MERGE_LEFT_COLOR, [px, y, mx-px, font_height - 1])
  pg.draw.rect(screen, MERGE_RIGHT_COLOR, [mx, y, qx-mx, font_height - 1])
  annotation(level, p, '[s')
  annotation(level, m + 0.5, 'm')
  annotation(level, q, 'e]')

def quicksort_push(left, right):
  global max_partition
  partitions.append((left+1, left, right+1, right, left, False))
  size = len(partitions)
  if max_partition < size:
    max_partition = size
  partition_show()
  wait(300)

def quicksort_draw_level(index):
  level = len(partitions) - index
  y = base_y - level * font_height
  l1, l2, r1, r2, p, fixed = partitions[index]

  lx = l1 * unit
  lw = (l2 - l1 + 1) * unit
  if lw > 0:
    color = QUICK_FIXED_COLOR if fixed else MERGE_LEFT_COLOR
    pg.draw.rect(screen, color, [lx, y, lw, font_height - 1])
    annotation(level, l2, '>')
  rx = r1 * unit
  rw = (r2 - r1 + 1) * unit
  if rw > 0:
    pg.draw.rect(screen, MERGE_RIGHT_COLOR, [rx, y, rw, font_height - 1])
    annotation(level, r1, '<')

  px = p * unit
  pw = unit
  pg.draw.rect(screen, BACK_COLOR, [px, y, pw, font_height])
  value = (p + 1) if selection else the_array[p]
  annotation(level, p, str(value))

def set_left(left):
  index = len(partitions) - 1
  l1, l2, r1, r2, p, fixed = partitions[index]
  partitions[index] = l1, left, r1, r2, p, fixed
  quicksort_draw_level(index)
  wait(WAIT_QUICK_SET_MILLIS)

def set_right(right):
  # print('right:', right)
  index = len(partitions) - 1
  l1, l2, r1, r2, p, fixed = partitions[index]
  partitions[index] = l1, l2, right, r2, p, fixed
  quicksort_draw_level(index)
  wait(WAIT_QUICK_SET_MILLIS)

def set_pivot(pivot):
  index = len(partitions) - 1
  l1, l2, r1, r2, p, fixed = partitions[index]
  partitions[index] = l1-1, pivot - 1, pivot + 1, r2, pivot, fixed
  quicksort_draw_level(index)
  wait(WAIT_QUICK_PIVOT_MILLIS)

def quicksort_fixed():
  index = len(partitions) - 1
  l1, l2, r1, r2, p, fixed = partitions[index]
  partitions[index] = l1, l2, r1, r2, p, True

def merge(list, index):
  draw_elem(list, index, MERGED_COLOR)
  pg.display.flip()
  wait(500)
  draw_elem(list, index, BACK_COLOR)
  draw_elem(None, index, BACK_COLOR, level = MERGED_LEVEL, value='')
  pg.display.flip()

MERGED_LEVEL = 1
def merged(list, left, index, merged):
  erase_level(MERGED_LEVEL)
  draw_elem(list, index, MERGED_COLOR)
  x = left * unit
  for i in range(len(merged)):
    draw_elem(merged, i, MERGED_COLOR, level = MERGED_LEVEL, x=x)
    x += unit
  pg.display.flip()
  wait(WAIT_MERGE_MILLIS)
  draw_elem(list, index, BACK_COLOR)

def erase_merged():
  erase_level(1)
  erase_level(MERGED_LEVEL)

def heap_set_root(root):
  global heap_root
  heap_root = root

compare_i1, compare_i2 = None, None
def heap_compare(list, i1, i2, root, size):
  global compare_i1, compare_i2
  compare_i1 = i1
  compare_i2 = i2
  heapsort(list, root, size)
  compare(list, i1, i2)
  compare_i1 = None
  compare_i2 = None
  heapsort(list, root, size)

def heapsort(list, root, size):
  global max_partition
  count = len(list)
  height = math.ceil(math.log2(count))
  if max_partition < height: max_partition = height

  eh = max_partition * font_height
  sw = screen_size[0]
  back_rect = [0, base_y - eh, sw, eh]
  # print(':erase:', back_rect)
  pg.draw.rect(screen, BACK_COLOR, back_rect)
  # wait(1000)

  hf = font_height // 2
  index = 0
  level = height
  lv_idx = 0
  lv_max = 1
  next_max = 2
  y = base_y - font_height * level + font_height // 2
  while index < count:
    # print(index, list[index])
    x = sw // next_max
    dx = x * 2
    # print(lv_max)
    while lv_idx < lv_max:
      if index > 0:
        dir = -1 if index % 2 == 0 else 1
        px = x + dir * dx // 2
        py = y - font_height // 2
        # print('yes:', index, size, kkk)
        # wait(1000)
        if index < size:
          # print('--drawing edge', index)
          pi = (index - 1) // 2
          if list[index] < list[pi]:
            edge = EDGE_GOOD_COLOR
          else:
            edge = EDGE_BAD_COLOR
          pg.draw.aaline(screen, edge, [x, y], [px, py])
        # else:
        #   print('--not drawing edgei', index)

      if index == heap_root:
        color = HEAP_ROOT_COLOR
      elif index == compare_i1 or index == compare_i2:
        color = COMPARE_COLOR
      elif index == root:
        color = HEAP_CURR_ROOT_COLOR
      else:
        color = BACK_COLOR
      pg.draw.circle(screen, color, [x, y], hf)
      pg.draw.circle(screen, EDGE_COLOR, [x, y], hf, 1)

      draw_text(font, str(list[index]), [x, y], TEXT_COLOR)
      index += 1
      if index >= count: break
      x += dx
      lv_idx += 1
    lv_idx = 0
    lv_max = next_max
    next_max *= 2
    y += font_height

  pg.display.flip()

if __name__ == '__main__':
  init('test')
  ll = list(range(10))
  setup(ll)
  draw_elem(ll, 7, SWAP_COLOR_1, 1)
  draw_elem(ll, 7, SWAP_COLOR_2, x=123, level=1)
  for level in range(1, 5+1):
    annotation(level, level, 'Level %d' % level)
  compare(ll, 1, 5)
  for level in range(3, 4+1):
    annotation(level, level)
  swap(ll, 1, 5)
  end()

