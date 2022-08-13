from vis.base import *

class Dog(Animal):
  def __init__(self):
    super().__init__()
    self.hello = 30
    self.world = 40

  def func(self, value):
    return self.hello + value

  def bark(self):
    return 'bark'

class Jindogae(Dog):
  def bark(self):
    return 'meong'
