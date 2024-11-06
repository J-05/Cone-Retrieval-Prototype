import math

# setting range of map for testing purposes
MIN = 100 # for both x and y
MAX = -100
STEP = 10 # intervals that cones snap to

map = {}
'''
^
map of cones, key is (x, y) of interval cones snap to, value is list of cones in that interval
e.g 
(40, 20) : [(43.2, 29.1), (40.1, 20.5)]

---

to find the interval of a cone, you just round towards 0 to the nearest multiple of STEP, 
e.g -43.2 -> -40, 29.1 -> 20
'''

##### generate test data #####

import random

cones = [] # list of randomly generated cones to be added to the map later

for _ in range(100):
    cones.append((random.uniform(MIN, MAX), random.uniform(MIN, MAX)))

# functions
def round_down(x, step=1):
    return int((x // step) * step)

def round_up(x, step=1):
    return int((((x // step) + (0 if x % step == 0 else 1))) * step)

def round_towards(target, x, step=1): # round towards target, step defines what multiple to round to 
    if x >= target:
        return round_down(x, step=step)
    if x < target:
        return round_up(x, step=step)
    
def find_a_pythagoras(b, c): # find a in pythagoras theorem a^2 + b^2 = c^2
    '''
    use this function to find what range of x values are in range of a given y value 
    (for a circle, as y moves futher from origin of cirle, the x interval/width of circle decreases)
    '''
    if c**2 < b**2: # if c is smaller than b (delta y), then the max val a (delta x) can be is c (radius)
        return c
    return (c**2 - b**2) ** (1/2)

def unzip_tuples(pairs):
    return [x[0] for x in pairs], [x[1] for x in pairs]

# add cones to map

for cone in cones:
    x, y = cone[0], cone[1]
    map.setdefault((round_down(x, STEP), round_down(y, STEP)), []).append(cone)

# show all cones in map

for key, val in map.items():
    print(f"{key}: {val}")

# generate random car

# car = (random.uniform(MIN, MAX), random.uniform(MIN, MAX))
car = (-40.5, 15.5)

radius = 30 # radius we are interested in

# keep cones within radius, and points we are checking to plot on graph
in_range = []
checking = []

#check for cones in range

def get_distance(point1, point2):
    delta_y = point1[1] - point2[1]
    delta_x = point1[0] - point2[0]

    return (delta_x**2 + delta_y**2)**1/2

def coords_within_range(origin, test, range):
    return range >= get_distance(origin, test)

print("Checking cones in range")
print(f"Car is at: {car}")

# main loop

'''
current optimisation issues:
- checking snap point of car twice
'''

for i in range(2): # positive y and negative y
    multiplier_y = (-1)**i
    bound_y = round_towards(car[1], car[1] + radius * multiplier_y, STEP) 
    min_y = round_towards(car[1], car[1], STEP)
    max_y = bound_y + STEP * multiplier_y # ensure edge of range is checked
    for y_snap in range(min_y, max_y, STEP * multiplier_y):
        y_reach = abs(y_snap - car[1])
        x_maxreach = find_a_pythagoras(y_reach, radius)
        # search along y row for x values in range
        for j in range(2): # positive x and negative x
            multiplier_x = (-1)**j
            bound_x = round_towards(car[0], car[0] + x_maxreach * multiplier_x, STEP)
            min_x = round_towards(car[0], car[0], STEP)
            max_x = bound_x + STEP * multiplier_x # ensure edge of range is checked
            for x_snap in range(min_x, max_x, STEP * multiplier_x):
                checking.append((x_snap, y_snap))
                if (x_snap, y_snap) in map.keys():
                    print(f"{map[(x_snap, y_snap)]} is a cone within the range")
                    in_range = in_range + map[(x_snap,y_snap)]
                    # for now its printing all cones that snap to the snap point
                    # need to add checks for snap points at the edge of the circle

# plot points
import matplotlib.pyplot as plt

x_axis, y_axis = unzip_tuples(cones)
plt.scatter(x_axis, y_axis) # all cones in blue

x_axis, y_axis = unzip_tuples(in_range)
plt.scatter(x_axis, y_axis, c="red") # cones detected in the range in red

x_axis, y_axis = unzip_tuples(checking)
plt.scatter(x_axis, y_axis, c="yellow", alpha=0.5) # all "snap" points checked in yellow

plt.scatter([car[0]], [car[1]], c="black") # car in black

plt.show()
# %%
