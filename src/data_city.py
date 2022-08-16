class City:
  def __init__(self, name, x, y, index=0):
    self.name = name
    self.x, self.y = x, y
    self.index = index
  def __repr__(self):
    return f'{self.name}({self.index}:{self.x:3d},{self.y:3d})'
  @staticmethod
  def apply_index(cities):
    for i in range(len(cities)): 
      cities[i].index = i


five_letter_cities = [
  City("Clean", 1336, 536, 0),
  City("Prosy", 977, 860, 1),
]

if __name__ == '__main__':
  # City.apply_index(five_letter_cities)
  print(f'{len(five_letter_cities)=}')
  print(f'Samples: {five_letter_cities[:100]}')

