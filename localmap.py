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

to find the interval of a cone, you round down to the nearest multiple of STEP, 
e.g -43.2 -> -50, 29.1 -> 20
'''

##### generate test data #####

import random

cones = [] # list of randomly generated cones to be added to the map later

for _ in range(100):
    cones.append((random.uniform(MIN, MAX), random.uniform(MIN, MAX)))

# functions
def round_down(x, interval=1):
    return int((x // interval) * interval)
    
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

#check if specific cones are in range

def get_distance_between_coords(point1, point2):
    delta_y = point1[1] - point2[1]
    delta_x = point1[0] - point2[0]

    return (delta_x**2 + delta_y**2)**1/2

def coords_within_range(a, b, range):
    return range >= get_distance_between_coords(a, b)

print("Checking cones in range")
print(f"Car is at: {car}")

# main loop

min_y_snap = round_down(car[1] - radius, STEP)
max_y_snap = round_down(car[1] + radius, STEP)

for y_snap in range(min_y_snap + STEP, max_y_snap, STEP): #excluding edge snap-points
    y_reach = abs(y_snap - car[1])
    x_maxreach = find_a_pythagoras(y_reach, radius)

    # search along y level for x values in range (excluding edge snap-points)
    min_x_snap = round_down(car[0] - x_maxreach, STEP)
    max_x_snap = round_down(car[0] + x_maxreach, STEP)
    for x_snap in range(min_x_snap + STEP, max_x_snap, STEP):
        checking.append((x_snap, y_snap))
        if (x_snap, y_snap) in map.keys():
            in_range = in_range + map[(x_snap,y_snap)]

# edge snap-points, have to check if each cone is within range
for y_snap in range(min_y_snap, max_y_snap + STEP, STEP):
    y_reach = abs(y_snap - car[1])
    x_maxreach = find_a_pythagoras(y_reach, radius)

    min_x_snap = round_down(car[0] - x_maxreach, STEP)
    max_x_snap = round_down(car[0] + x_maxreach, STEP)
    for x_snap in [min_x_snap, max_x_snap]:
        checking.append((x_snap, y_snap))
        if (x_snap, y_snap) in map.keys():
            for cone in map[(x_snap,y_snap)]:
                if coords_within_range(car, cone, radius):
                    in_range.append(cone)

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
