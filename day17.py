from parsy import string, char_from, regex, seq
import time

data = 'target area: x=14..50, y=-267..-225'
example = 'target area: x=20..30, y=-10..-5'

number_literal = regex(r'-?[0-9]+').map(int)
range_literal = seq(number_literal, string('..') >> number_literal).map(tuple)
target_def = seq(string('target area: x=') >> range_literal, string(', y=') >> range_literal)


targets_x, targets_y = target_def.parse(data)
#print(targets_x, targets_y)


def ballistic_step(pos, vel):
    pos = pos[0] + vel[0], pos[1] + vel[1]
    vel = max(vel[0] - 1, 0), vel[1] - 1

    return pos, vel



def min_x_to_hit_target(targets_x):
    for i in range(targets_x[1]):
        if targets_x[0] <= i * (i + 1) // 2 <= targets_x[1]:
            return i
 
    raise Exception("Can't hit target")


def can_hit_target(pos, vel, targets_x, targets_y):
    while True:
        #print(pos, vel)
        if targets_x[0] <= pos[0] <= targets_x[1] and targets_y[0] <= pos[1] <= targets_y[1]:
            return True
        
        pos, vel = ballistic_step(pos, vel)
        #max_height = max(max_height, pos[1])
        if vel[0] == 0 and pos[0] < min(targets_x):
            return False
            #raise Exception("Fall short of box")

        if pos[0] > max(targets_x):
            return False
            #raise Exception("Overshot box")

        if pos[1] < min(targets_y):
            return False
            #raise Exception("We're already below target")


    #time.sleep(0.1)


pos = (0, 0)
vel = (6, 20)
max_height = 0
min_x = min_x_to_hit_target(targets_x)
vel = (min_x, 20)

def test_ys(targets_x, targets_y):
    pos = (0,0)
    min_x_vel = min_x_to_hit_target(targets_x)
    max_y = targets_y[1]

    for vel_y in range(targets_y[1], 1000):
        #print(f'testing {vel_y=}')
        vel = (min_x_vel, vel_y)
        if can_hit_target(pos, vel, targets_x, targets_y):
            max_y = vel_y

    return max_y * (max_y + 1) // 2

def test_all(targets_x, targets_y):
    pos = (0, 0)
    hits = 0
    min_x_vel = min_x_to_hit_target(targets_x)
    print(f'{min_x_vel=}')


    for vel_x in range(min_x_vel, max(targets_x)+1):
        for vel_y in range(-1000, 1000):
            vel = (vel_x, vel_y)
            if can_hit_target(pos, vel, targets_x, targets_y):
                print(vel)
                hits += 1

    return hits


print('part 1', test_ys(targets_x, targets_y))
print('part 2', test_all(targets_x, targets_y))

print(can_hit_target(pos, vel, targets_x, targets_y))