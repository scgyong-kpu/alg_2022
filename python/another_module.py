
def world():
  print('이거는 another_module 에 들어 있는 world 함수 입니다')

def set_something(some):
  global value
  value = some * 2

def get_something():
  return value

class CrazyDog:
  def bark(self):
    print("미친개는 야옹야옹")

