
array = [45,20,35,60,55,10,90,85,25,75]
max = float('-inf')
at = -1
for i in range(len(array)):
  if max < array[i]:
    max = array[i]
    at = i
print(f'{max=}, {at=}')


