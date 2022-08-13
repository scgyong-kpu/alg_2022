from unsorted import numbers as orig

numbers = orig[:100]
arr = []
for i in range(1, 100 + 1):
  if i in numbers:
    pass
    # print(i)
  else:
    arr.append(i)

ss = sorted(numbers)
for i in range(0, 100, 10):
  print(ss[i:i+10])
while len(numbers) > 0:
  n = numbers.pop(0)
  if n in numbers:
    print(n)

print(arr)

# 1
# 25
# 28
# 32
# 36
# 43
# 49
# 50
# 53
# 58
# 73
# 78
# 99