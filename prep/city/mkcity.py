from oxford_words import five_letters
from random import randint
from math import sqrt

count = 1000
coord_start = 1
coord_end_x = 1599
coord_end_y = 899
MIN_DIST = 30

fives = five_letters[:count]
coords = []

def distance(c1, c2):
  dx, dy = c1[0] - c2[0], c1[1] - c2[1]
  return sqrt(dx ** 2 + dy ** 2)

def make_coord():
  loop = True
  while loop:
    x, y = randint(coord_start, coord_end_x), randint(coord_start, coord_end_y)
    loop = False
    for co in coords:
      dist = distance((x, y), co)
      # print(dist)
      if dist < MIN_DIST:
        # print(dist)
        loop = True
        break
  return x, y


for word in fives:
  name = word.capitalize()
  x, y = make_coord()
  coords.append((x, y))
  print('  City("%s", %d, %d),' % (name, x, y))
