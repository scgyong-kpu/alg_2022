
def world():
  print('이거는 hello module 에 들어 있는 world 함수 입니다')

def set_something(some):
  global value
  value = some

def get_something():
  return value

class Dog:
  def bark(self):
    print("Dog 가 짖는다 bark bark")

class Jindogae(Dog):
  def bark(self):
    print("진도개는 멍멍하고 짖는다")

