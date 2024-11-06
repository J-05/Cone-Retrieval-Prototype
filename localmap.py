import math

MIN = 100
MAX = -100
STEP = 10

# generate test data

import random

map = {}
cones = []

for _ in range(100):
    cones.append((random.uniform(MIN, MAX), random.uniform(MIN, MAX)))

# functions

def round_down(x, step=1):
    return int(((x // step) + (1 if x < 0 else 0)) * step)

def find_a_pythagoras(b, c):
    if c**2 < b**2:
        return c
    return (c**2 - b**2) ** (1/2)

def unzip_tuples(pairs):
    return [x[0] for x in pairs], [x[1] for x in pairs]

# add cones to map

for cone in cones:
    x, y = cone[0], cone[1]
    map.setdefault((round_down(x, STEP), round_down(y, STEP)), []).append(cone)

# show all cones in map

print("map")
for key, val in map.items():
    print(f"{key}: {val}")

# generate random car

# car = (random.uniform(MIN, MAX), random.uniform(MIN, MAX))
car = (-40.5, 15.5)
print(f"Car is at: {car}")

radius = 30 # radius we are interested in

# keep cones in range and points we are checking to plot on grapth
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

for i in range(2): # positive y and negative y
    multiplier_y = (-1)**i
    bound_y = round_down(car[1] + radius * multiplier_y, STEP) 
    min_y = round_down(car[1], STEP)
    max_y = bound_y + STEP * multiplier_y # ensure edge of range is checked
    for j in range(2): # positive x and negative x
        multiplier_x = (-1)**j
        for y_snap in range(min_y, max_y, STEP * multiplier_y):
            y_reach = abs(y_snap - car[1])
            print(f"Checking y_reach: {y_reach}")
            x_maxreach = find_a_pythagoras(y_reach, radius)
            print(f"Checking x_maxreach: {x_maxreach}")
            # search along y row for x values in range
            bound_x = round_down(car[0] + x_maxreach * multiplier_x, STEP)
            print(f"Checking bound_x: {bound_x}")
            min_x = round_down(car[0], STEP)
            print(f"Checking min_x: {min_x}")
            max_x = bound_x + STEP * multiplier_x # ensure edge of range is checked
            print(f"Checking max_x: {max_x}")
            for x_snap in range(min_x, max_x, STEP * multiplier_x):
                print(f"Checking x_snap: {x_snap}")
                checking.append((x_snap, y_snap))
                if (x_snap, y_snap) in map.keys():
                    print(f"{map[(x_snap, y_snap)]} is a cone within the range")
                    in_range = in_range + map[(x_snap,y_snap)]

# plot points
import matplotlib.pyplot as plt

x_axis, y_axis = unzip_tuples(cones)
plt.scatter(x_axis, y_axis)

x_axis, y_axis = unzip_tuples(in_range)
plt.scatter(x_axis, y_axis, c="red")

x_axis, y_axis = unzip_tuples(checking)
plt.scatter(x_axis, y_axis, c="yellow", alpha=0.5)

plt.scatter([car[0]], [car[1]], c="black")

plt.show()