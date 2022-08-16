class City:
  def __init__(self, name, x, y, index=0):
    self.name = name
    self.x, self.y = x, y
    self.index = index
  def __repr__(self):
    return f'{self.name}({self.index}:{self.x:3d},{self.y:3d})'

five_letter_cities = [
  City("Clean", 1336, 536),
  City("Prosy", 977, 860),
]

if __name__ == '__main__':
  print(five_letter_cities)

