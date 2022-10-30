from data_city import City, five_letter_cities
from vis import KruskalVisualizer as Visualizer

if __name__ == '__main__':
  vis = Visualizer('Minimum Spanning Tree - Ksuskal')
  cities = five_letter_cities[:20]
  City.apply_index(cities)
  vis.setup(vis.get_main_module())
  vis.draw()
  vis.end()
    # again = vis.end()
    # if not again: break
