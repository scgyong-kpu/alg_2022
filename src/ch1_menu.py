import ch1_1_find_max as finder

while True:
  v = input('Enter menu:') # input() 때문에 sublime text 에서는 실행할 수 없으니 cmd 창에서 할 것
  if v == '1':
    max, at = finder.find_max([90, 85, 75, 60, 55, 45, 35, 25, 20, 10])
    print(f'{max=}, {at=}')
  elif v == '2':
    max, at = finder.find_max([1,54,12,4,2,34,5,23,543,23,32,53,23,3])
    print(f'{max=}, {at=}')
  else:
    break
