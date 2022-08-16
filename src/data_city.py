class City:
  def __init__(self, name, x, y, index=0):
    self.name = name
    self.x, self.y = x, y
    self.index = index
  def __repr__(self):
    return '%s(%d:%3d,%3d)' % (self.name, self.index, self.x, self.y)

five_letter_cities = [
  City("Clean", 1336, 536),
  City("Prosy", 977, 860),
]
