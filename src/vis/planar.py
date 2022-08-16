import math
from vis.base import *

clr = Color()
clr.city_body = Color.pastel2[0]
clr.city_line = Color.set2[0]
clr.city_name = Color.set3[0]
clr.edge_value = color_argb('#1f3f1f')
ctx_city_normal = {
  'city_body_color': Color.pastel2[0],
  'city_line_color': Color.set2[0],
  'city_name_color': Color.set1[1],
  # 'shows_city_index': True,
  # 'shows_city_coord': True,
}

ctx_city_grayed = {
  'city_body_color': Color.gray[0],
  'city_line_color': Color.gray[1],
  'city_name_color': Color.gray[1],
}

ctx_city_compare = {
  'city_body_color': Color.pastel2[1],
  'city_line_color': Color.set2[1],
  'city_name_color': Color.dark[1],
}
ctx_city_mark = {
  'city_body_color': Color.pastel2[2],
  'city_line_color': Color.set2[2],
  'city_name_color': Color.dark[2],
}
ctx_city_update = {
  'city_body_color': Color.pastel2[3],
  'city_line_color': Color.set2[3],
  'city_name_color': Color.dark[3],
}

city_contexts = [
  ctx_city_grayed, ctx_city_normal, ctx_city_compare, ctx_city_mark, ctx_city_update
]

ctx_edge_grayed = {
  'edge_line_color': Color.gray[0],
  'edge_value_color': Color.gray[1],
}

ctx_edge_normal = {
  'edge_line_color': clr.line,
  'edge_value_color': clr.edge_value,
}

ctx_edge_compare = {
  'edge_line_color': Color.pastel2[1],
  'edge_value_color': Color.set2[1],
}
ctx_edge_mark = {
  'edge_line_color': Color.pastel2[2],
  'edge_value_color': Color.set2[2],
}
ctx_edge_update = {
  'edge_line_color': Color.pastel2[3],
  'edge_value_color': Color.set2[3],
}
edge_contexts = [
  ctx_edge_grayed, ctx_edge_normal, ctx_edge_compare, ctx_edge_mark, ctx_edge_update
]

# t = 0.0 ~ 2.0 사이로 변화하는 값임. 1 이면 가운데임
def lerp_2d(xy1, xy2, t=1):
  # x1,y1 = xy1[0], xy1[1]
  # x2,y2 = xy2[0], xy2[1]
  x1,y1,x2,y2 = *xy1, *xy2
  return [(x1*(2-t)+x2*t)//2, (y1*(2-t)+y2*t)//2]

# 평면 시각화
class PlanarVisualizer(Visualizer):
  LEVEL_GRAYED, LEVEL_NORMAL, LEVEL_COMPARE, LEVEL_MARK, LEVEL_UPDATE, LEVELS_COUNT = range(6)
  def setup(self, data):
    self.data = data
    self.compute_min_max()
    self.city_levels = dict()
    # self.draw()

  def compute_min_max(self):
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    for c in self.data.cities:
      if min_x > c.x: min_x = c.x
      if min_y > c.y: min_y = c.y
      if max_x < c.x: max_x = c.x
      if max_y < c.y: max_y = c.y
    # print('min:', (min_x, min_y), 'max:', (max_x, max_y))
    self.min_x, self.max_x = min_x, max_x
    self.min_y, self.max_y = min_y, max_y

    self.diff_x = max_x - min_x
    self.diff_y = max_y - min_y

  def set_city_level(self, index, level):
    self.city_levels[index] = level

  def draw(self):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()

  def draw_content(self):
    if hasattr(self.data, 'edges'):
      self.draw_all_edges(shows_edge_value=True, **ctx_edge_normal)
    self.draw_all_cities()

  def calc_coords(self):
    cw = self.config.screen_width - 2 * self.separator_size
    ch = self.config.screen_height - 2 * self.separator_size

    scale_x, scale_y = cw / self.diff_x, ch / self.diff_y
    if scale_x < scale_y:
      self.scale = scale_x
      self.diff = self.diff_x
    else:
      self.scale = scale_y
      self.diff = self.diff_y

    self.city_radius = self.config.font_size // 3

  def o2s(self, x, y):
    dx, dy = x - self.min_x, y - self.min_y
    x = self.separator_size + dx * self.scale
    y = self.separator_size + dy * self.scale
    # print(f'{self.diff=} {self.scale=} {(dx,dy)=}  {(x,y)=}')
    return [x, y]

  def xy2s(self, xy):
    return self.o2s(xy[0], xy[1])

  def city2s(self, city):
    return self.xy2s([city.x, city.y])

  def draw_all_cities(self, **args):
    for i in range(len(self.data.cities)):
      level = self.city_levels[i] if i in self.city_levels else 1
      self.draw_city(i, **city_contexts[level], **args)

  def draw_all_edges(self, **args):
    for edge in self.data.edges:
      self.draw_edge(*edge, **args)
      # self.draw_directed_edge(*edge, **args)
      # self.draw_directed_edge(u,v,w, **args)
      # self.draw_directed_edge(v,u,w, **args)

  def draw_city(self, city, **args):
    if isinstance(city, int):
      city = self.data.cities[city]
    xy = self.xy2s([city.x, city.y])
    body_color = attr(args, 'city_body_color', clr.city_body)
    line_color = attr(args, 'city_line_color', clr.city_line)
    name_color = attr(args, 'city_name_color', clr.city_name)

    radius = self.city_radius
    pg.draw.circle(self.screen, body_color, xy, radius)
    pg.draw.circle(self.screen, line_color, xy, radius, 1)

    xy[1] -= self.config.font_size // 2 + radius
    name = city.getName(**args)

    # print(city, name)
    self.draw_text(name, xy, text_color=name_color, **args)

  def draw_edge(self, c1, c2, value=None, **args):
    if isinstance(c1, int): c1 = self.data.cities[c1]
    if isinstance(c2, int): c2 = self.data.cities[c2]
    xy1, xy2 = self.city2s(c1), self.city2s(c2)
    line_color = attr(args, 'edge_line_color', clr.line)
    pg.draw.aaline(self.screen, line_color, xy1, xy2)
    if value != None:
      shows_value = attr(args, 'shows_edge_value', False)
      if shows_value:
        xy = lerp_2d(xy1, xy2)
        value_color = attr(args, 'edge_value_color', clr.edge_value)
        # print(f'{value_color=} {clr.edge_value=} {args=}')
        self.draw_text(f'{value}', xy, text_color=value_color)

  def draw_directed_edge(self, c1, c2, value=None, **args):
    if isinstance(c1, int): c1 = self.data.cities[c1]
    if isinstance(c2, int): c2 = self.data.cities[c2]
    x1,y1,x2,y2 = *self.city2s(c1), *self.city2s(c2)
    angle = math.atan2(y2-y1, x2-x1)
    shift_angle = angle + math.pi / 2
    radius = self.city_radius // 2
    shift_x = radius * math.cos(shift_angle)
    shift_y = radius * math.sin(shift_angle)
    sxy, dxy = self.shorter_line(x1+shift_x, y1+shift_y, x2+shift_x, y2+shift_y, angle)
    self.draw_arrow(sxy, dxy, angle, value, **args)

  def draw_arrow(self, sxy, dxy, angle=None, value=None, **args):
    line_color = attr(args, 'edge_line_color', clr.line)
    axy = self.get_arrow_pos(sxy, dxy, angle)
    pg.draw.aaline(self.screen, line_color, sxy, dxy)
    pg.draw.aaline(self.screen, line_color, dxy, axy)

    print(f"{value=} {attr(args, 'shows_edge_value', False)=}")

    if value != None:
      shows_value = attr(args, 'shows_edge_value', False)
      if shows_value:
        xy = lerp_2d(sxy, dxy, 1.1) # at 55% position (1=50%, 2=100%)
        value_color = attr(args, 'edge_value_color', clr.edge_value)
        self.draw_text(f'{value}', xy, text_color=value_color)

  def shorter_line(self, x1,y1,x2,y2,angle=None):
    diff = 2 * self.city_radius
    if angle == None:
      angle = math.atan2(y2-y1, x2-x1)
    dx = diff * math.cos(angle)
    dy = diff * math.sin(angle)
    return [x1+dx,y1+dy], [x2-dx,y2-dy]

  def get_arrow_pos(self, xy1, xy2, angle=None):
    length = 2 * self.city_radius
    x1,y1 = xy1
    x2,y2 = xy2
    if angle == None:
      angle = math.atan2(y2-y1, x2-x1)
    angle += math.pi * 5 / 6 # 150 degree
    ax = x2 + length * math.cos(angle)
    ay = y2 + length * math.sin(angle)
    return [ax, ay]

