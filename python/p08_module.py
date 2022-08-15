#python 에는 많은 내장 모듈이 있다
import math
pt1, pt2 = [ -150, -100 ], [ 150, 300 ]
distance = math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
print(f'두 점 {pt1} 과 {pt2} 사이의 거리는 {distance:.2f} 이다')

# 두 점이 이루는 각도를 구하려면 atan(y/x) 을 사용해야 한다
# 하지만 부호도 신경써야 하므로 atan2(y, x) 를 쓰면 알아서 해 준다
angle_radian = math.atan2((pt2[1]-pt1[1]), (pt2[0]-pt1[0]))

# Computer Graphics 는 대부분 radian 단위를 사용한다. 사람이 이해할 때는 Degree 가 편할때가 많다
angle_degree = 180 * angle_radian / math.pi

print(f'두 점 사이의 선이 만드는 각도는 Radian 으로는 {angle_radian:.2f}, Degree 로는 {angle_degree:.2f}° 이다')

# 길이를 알 때 각도만큼 회전했을 때의 좌표를 알려면 x 좌표는 cos, y 좌표는 sin 을 쓴다
dx = distance * math.cos(2 * angle_radian)
dy = distance * math.sin(2 * angle_radian)

pt3 = [pt1[0] + dx, pt1[1] + dy]
print(f'pt1 을 기준으로 {angle_degree:.2f}° 만큼 더 회전한 점은 [{pt3[0]:.2f}, {pt3[1]:.2f}] 이다')

print()
# 반올림=round, 버림=floor (바닥), 올림=ceil (천장)
print(f'{angle_radian=} {round(angle_radian)=} {math.floor(angle_radian)=} {math.ceil(angle_radian)=}')

# round 의 두번째 인자를 통해서 몇째자리에서 반올림할지 결정할 수 있다
PIx100 = math.pi * 100
print(f'{PIx100=} {round(PIx100, 2)=} {round(PIx100, -2)=}')

print()
import random
print(f'0~1 사이의 랜덤한 숫자 세개 출력: {random.random()} {random.random()} {random.random()}')
print(f'[10,15) 랜덤한 정수 세개 출력: {random.randrange(10, 15)} {random.randrange(10, 15)} {random.randrange(10, 15)}')
print(f'[10,15] 랜덤한 정수 세개 출력: {random.randint(10, 15)} {random.randint(10, 15)} {random.randint(10, 15)}')
# Python 에서는 대개 [inclusive, exclusive) 를 많이 쓰지만 randint 는 [inclusive, inclusive] 형태로 쓴다

candidates = [ 10, 100, 123, 456, 789 ]
print(f'배열 중에서 하나 골라준다: {random.choice(candidates)=}')
print(f'배열 중에서 여러 개 골라준다: {random.sample(candidates, 3)=}')

random.shuffle(candidates)
print(f'배열 내용을 섞어준다: {candidates=}')

