
# 중괄호와 : 을 사용하여 정의한다
d1 = {
  "hello": 10, "world": 20.5
}

print('-- Key 가 hello 인 항목의 value 는? --')
print(d1["hello"])

# 세 개의 key 에 대하여 그 값을 알아보자 가능한가?
keys = [ "hello", "are_you_there", "world" ]
for key in keys:
  print('-- Key:', key)

  value = d1[key] if key in d1 else '없는데요'
  # if key in d1:
  #   value = d1[key]
  # else:
  #   value = '없는데요'

  print('--- Value:', value)

# C/C++/Java 등에서 사용하는 3항연산자 a ? b : c 를
# python 에서는 b if a else c 형태로 사용한다
# 조금 더 영어문장스럽게 사용한다고 할 수 있다

words = [
  "flagrant",
  "lawmaker",
  "allow",
  "alumina",
  "foxglove",
  "fiche",
  "concern",
  "kiosk",
  "clean",
  "especially",
  "wanton",
  "addle",
  "agitate",
  "whinchat",
]

print()
print('-- 각 글자별로 시작하는 단어가 몇개 있는제 세는 프로그램 --')
counts = dict() # Dictionary 를 초기화한다
for word in words: # 모든 단어들에 대하여
  first_ch = word[0] # 단어의 첫글자를 알아낸 뒤
  if not first_ch in counts: # Dictionary 에 해당 Key 가 없으면 
    counts[first_ch] = 0      # 만들고 0 으로 초기값을 준다
  counts[first_ch] += 1      # 해당 Key 의 Value 를 1 증가시킨다 

# for ch in counts.keys():
#   print(ch, counts[ch])
print(counts)

print()
print('-- Dictionary 는 빨리 찾는 게 가장 중요한 구조라서 Key 들이 정렬되어 있지 않다 --')
print('-- 하지만 Python 3.6 이후부터는 추가 순서가 보장된다 --')
print('-- Key 들을 정렬한 뒤에 루프를 돌아도 좋지만, 보통 그럴 일은 잘 없다 --')
for ch in sorted(counts.keys()):
  print(ch, counts[ch])

print()
print('-- 매번 Key 가 있는지 찾아보는 것이 귀찮을 때가 있다. 이럴때는 defaultdict 를 쓴다--')
print('-- defaultdict(XXX) 로 생성된 것은 Key 가 존재하지 않으면 XXX() 로 값을 만든다--')
from collections import defaultdict # import collections 라고 했다면
counts2 = defaultdict(int)          # collections.defaultdict 라고 써야 한다
for word in words: # 모든 단어들에 대하여
  first_ch = word[0] # 단어의 첫글자를 알아낸 뒤
  counts2[first_ch] += 1      # 해당 Key 의 Value 를 1 증가시킨다 
print(counts2)

print('-- 존재하지 않는 Key 가 들어오면 int() 즉 0 값이 들어 있었던 것으로 간주한다')
print(int(), counts2['hello']) # 둘 다 모두 0 값이 된다
print(counts2)
